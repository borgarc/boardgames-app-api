import time
from xml.etree import ElementTree

import requests
from django.db.models import Max

from game.models import BoardGame
from game.repositories.catalog_repository import CatalogRepository


class BGGCatalogRepository(CatalogRepository):
    def update_catalog(self):
        """
        batch_count: how many 20 packs of games we can use per execution.
        Deafult 200 games per execution.
        """
        batch_count = 10
        batch_size = 20

        session = self._set_headers()

        current_id = self._get_current_id()

        for _ in range(batch_count):
            end_id = current_id + batch_size
            ids_str = ",".join(str(i) for i in range(current_id, end_id))
            
            url = f"https://boardgamegeek.com/xmlapi2/thing?id={ids_str}&stats=1"
            
            try:
                response = session.get(url, timeout=20)
                if response.status_code == 200:
                    print(f"Success: Processing batch of IDs {ids_str}.")
                    self.parse_and_save_bgg_xml(response.content)
                    current_id = end_id
                    time.sleep(3)
                elif response.status_code == 401:
                    print("Error 401: Unauthorized. Token is invalid or expired.")
                    break
                elif response.status_code == 429:
                    print("Error 429: Too many requests. Rate limit hit. Waiting...")
                    time.sleep(60)
                    break
            except Exception as e:
                print(f"Connection error: {e}")
                break

    def parse_and_save_bgg_xml(self, xml_data):
        root = ElementTree.fromstring(xml_data)
        for item in root.findall('item'):
            # We wont save expansions or extras.
            if item.get('type') != 'boardgame':
                continue

            bgg_id = int(item.get('id'))
            name_node = item.find(".//name[@type='primary']")
            name = name_node.get('value') if name_node is not None else "Unknown"

            defaults = {
                'name': name,
                'description': getattr(item.find('description'), 'text', ""),
                'year_published': self._get_val(item, 'yearpublished'),
                'min_players': self._get_val(item, 'minplayers'),
                'max_players': self._get_val(item, 'maxplayers'),
                'playing_time': self._get_val(item, 'playingtime'),
                'image_url': getattr(item.find('image'), 'text', ""),
                'rating': self._get_rating(item),
            }

            BoardGame.objects.update_or_create(bgg_id=bgg_id, defaults=defaults)

    def _get_current_id(self):
        last_id_entry = BoardGame.objects.aggregate(Max('bgg_id'))['bgg_id__max']
        start_id = (last_id_entry + 1) if last_id_entry else 1
        
        current_id = start_id

        return current_id

    def _set_headers(self):
        BGG_TOKEN = ""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Authorization': f'Bearer {BGG_TOKEN}',
            'Accept': 'application/xml, text/xml, */*',
        }
        session = requests.Session()
        session.headers.update(headers)

        return session

    def _get_val(self, item, tag):
        node = item.find(tag)
        return node.get('value') if node is not None else None

    def _get_rating(self, item):
        rating_node = item.find(".//average")
        return float(rating_node.get('value')) if rating_node is not None else 0.0
