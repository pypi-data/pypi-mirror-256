from typing import Iterator, List, Dict, Union
from requests.exceptions import ConnectionError

import lxml.etree as etree
import folium
import geojson

from perdido.utils.disambiguation import clustering_disambiguation
from perdido.utils.webservices import WebService
from perdido.perdido import Perdido, PerdidoCollection
import spacy
from pandas.core.series import Series


class Geoparser:

    def __init__(self, api_key: str = "libPython", lang: str = 'fr', version: str = 'Standard', pos_tagger: str = 'spacy', sources: Union[List[str], None] = None, 
                max_rows: Union[int, None] = None, alt_names: Union[bool, None] = None, bbox: Union[List[float], None] = None, 
                country_code: Union[str, None] = None, geocoding_mode: Union[int, None] = None, disambiguation: Union[str, None] = None, input_format:str = 'txt') -> None:

        self.url_api = 'http://choucas.univ-pau.fr/PERDIDO/api/'
        self.serviceGeoparsing = 'geoparsing'

        self.lang = lang
        self.api_key = api_key
        self.version = version

        if self.version == 'GeoEDdA' : 
            self.pipeline = 'model'
        elif self.version == 'Standard' or self.version == 'Encyclopedie':
            self.pipeline = 'ws'
        else:
            self.version = 'Standard'
            self.pipeline = 'ws'

        self.pos_tagger = pos_tagger

        if sources is not None:
            self.sources = sources
        else:
            self.sources = ['nominatim']
            
        self.max_rows = max_rows
        self.alt_names = alt_names

        self.geocoding_mode = geocoding_mode

        self.country_code = country_code

        if bbox is not None and len(bbox) == 4:
            self.bbox = bbox
        else:
            self.bbox = None

        self.disambiguation = disambiguation
        self.input_format = input_format


    def __call__(self, content: Union[str, List[str], Series]) -> Union[Perdido, PerdidoCollection, None]:
        return self.parse(content)


    def parse(self, content: Union[str, List[str], Series], geom = None) -> Union[Perdido, PerdidoCollection, None]:
        
        if type(content) == str:
            if self.pipeline == 'ws':
                return self.call_perdido_ws(content, geom)
            if self.pipeline == 'model':
                if self.version == 'GeoEDdA':
                    return self.run_geoedda_model(content, geom)
        elif type(content) == list or type(content) == Series:
            collection = PerdidoCollection()
            if self.pipeline == 'ws':
                for c in content:
                    collection.append(self.call_perdido_ws(c, geom))
            if self.pipeline == 'model':
                if self.version == 'GeoEDdA':
                    for c in content:
                        collection.append(self.run_geoedda_model(c, geom))
            return collection
        else:
            return None


    def run_geoedda_model(self, content: str, geom = None) -> Perdido:
            
        res = Perdido()
        res.text = content
        res.geometry_layer = geom

        nlp = spacy.load("fr_spacy_custom_spancat_edda")
        nlp.add_pipe('sentencizer')

        doc = nlp("* ALBI, (Géog.) ville de France, capitale de  l'Albigeois, dans le haut Languedoc : elle est sur le Tarn. Long. 19. 49. lat. 43. 55. 44.")

        #res.tei = val
        #TODO: add geocoding process

        res.geojson = None
        if self.disambiguation == 'cluster':
            res.geojson, res.geojson_ambiguous, res.best_cluster = clustering_disambiguation(res)

        #res.parse_tei()

        return res, doc
    
        
    
    def call_perdido_ws(self, content: str, geom = None) -> Perdido:
        try:
            ws = WebService()

            parameters = {'api_key': self.api_key, 
                    #'content': content, 
                    'lang': self.lang, 
                    'version': self.version, 
                    'geocoding_mode': self.geocoding_mode, 
                    'max_rows': self.max_rows, 
                    'alt_names': self.alt_names,
                    'sources': self.sources,
                    'pos_tagger': self.pos_tagger,
                    'input_format': self.input_format}
            
            if self.bbox is not None:
                parameters['bbox'] = self.bbox
    
            if self.country_code is not None:
                parameters['country_code'] = self.country_code

            data = {'content': content}

            ws.post(self.serviceGeoparsing, params=parameters, data=data)

            res = Perdido()
            res.text = content
            res.geometry_layer = geom

            success, val = ws.get_result('xml-tei', 'xml')
            if success:
                res.tei = val

                success, val =  ws.get_result('geojson')
                if success:
                    res.geojson = val
            else:
                print(val)

            if self.disambiguation == 'cluster':
                res.geojson, res.geojson_ambiguous, res.best_cluster = clustering_disambiguation(res)

            res.parse_tei()

            return res
        except ConnectionError as e:
            print(e)
            return None

