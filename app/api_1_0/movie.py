
from ..api import Resource
from ..extensions import movie_datastore

class EpisodeResource(Resource):

    def read(self, id):
        return [
            {
                "sources": [
                  {
                    "file": "https://r5---sn-42u-nbos.googlevideo.com/videoplayback?requiressl=yes&id=5804432291bb7504&itag=18&source=webdrive&ttl=transient&app=explorer&ip=2405:4800:529c:c7a8:903a:6270:ce2a:b0e8&ipbits=0&expire=1473837766&sparams=expire,id,ip,ipbits,itag,mm,mn,ms,mv,pl,requiressl,source,ttl&signature=4ACA972D61A243D8C3269AC2FB363FFF7AC9C27B.0E358B218F0C7156E9C36F2F8FD6BF2D4E60C621&key=cms1&pl=46&cms_redirect=yes&mm=31&mn=sn-42u-nbos&ms=au&mt=1473823550&mv=m",
                    "type": "mp4",
                    "label": "360p"
                  }
                ],
                "tracks": []
            }
        ]

class MovieResource(Resource):
    def filter(self, type):
        pagination = OffsetPagination(movie_datastore.find_movie_list(),
                        limit=int(request.args.get('limit') or 10),
                        offset=int(request.args.get('offset') or 0))

        return pagination.data
