<template>
    <div>
        <div id='bg'/>
        <navBar/>
        <h2 style="font-size: 50px; color: white;">請選擇標籤</h2>
        <div id="tagTable_container">
            <tagTable :table_data='tags_data' :key='rerender' @send_tags='send_tags'/>
        </div>
    </div>
</template>

<script>
import navBar from '@/components/navBar'
import tagTable from '@/components/tag/tag_table'
import {getMe} from '@/apis/get_genre'
import {GetRecentlyPlayed} from '@/apis/get_recently_played'
import {GetUserPlaylists} from '@/apis/get_user_playlists'
import {GetFollowedArtist} from '@/apis/get_followed_artist'
import axios from 'axios'


export default {
    name: 'tags',
    components: {
        navBar,
        tagTable,
    },
    data() {
        return {
            // 從每個類別找到的genre會存成{genre: frequency}的格式
            genre_dict: {
                "album": {},
                "artist": {},
                "track": {}
            },

            // [artist_name, artist_id] in followed_artist
            followed_artist: [],
            recently_played:[],
            tags_data: [{
                'class': 'Genres',
                'tags': []
            }, {
                'class': 'Artists',
                'tags': []
            }, {
                'class': 'Tracks',
                'tags': []
            }],
            rerender: 0,
        }
    },
    created() {
        let urlParams = new URLSearchParams(window.location.search)
        this.$store.access_token = urlParams.get('access_token')
        this.$store.between_subject_type = urlParams.get('between_subject_type')
        this.$store.within_subject_type = urlParams.get('within_subject_type')
        this.$store.pass_exp_num = urlParams.get('pass_exp_num')

        console.log("tags between", this.$store.between_subject_type)
        console.log("tags within", this.$store.within_subject_type)

        // 每到 create list 或 選擇 seed 頁面，就增加做過的實驗數量(每個人應做兩次)
        this.$store.pass_exp_num+=1

        getMe(this.$store.access_token).then((res)=>{
            console.log('call me success')
            console.log(res.data)
        }).catch((err)=>{
            console.log('call me faild')
            console.log(err)
        })

        

        // 獲取使用者建立的播放清單
        GetUserPlaylists(this.$store.access_token).then((res)=>{
            console.log("Call GetUserPlaylists API successed!")
            let retv = res.data
            console.log(retv)
        })

        axios.all([this.WrapGetRecentlyPlayed(), this.WrapGetFollowedArtist()]).then(axios.spread(()=> {
            // set tags table items

            // 預設artist全部丟
            var followed_artist_name = this.followed_artist.map((elem)=> {
                return elem[0]
            })
            this.tags_data[1]['tags'] = followed_artist_name

            // 預設tracks丟前10個
            var track_name = this.recently_played.map((elem)=> {
                return elem[0]
            })

            this.tags_data[2]['tags'] = track_name.slice(0, 11)

            // 預設genres丟前10高的
            var genere_freq_lst = []

            //dict to 2d array
            for(var [key, val] of Object.entries(this.genre_dict['artist'])) {
                genere_freq_lst.push([key, val])
            }

            // sort by genere's frequency
            genere_freq_lst.sort((a, b)=> {
                return b[1]-a[1]
            })

            genere_freq_lst = genere_freq_lst.map((elem=>{
                return elem[0]
            }))

            this.tags_data[0]['tags'] = genere_freq_lst

        }))

    },
    methods: {
        WrapGetRecentlyPlayed() {
            // 獲取最近撥放的歌曲
            return GetRecentlyPlayed(this.$store.access_token).then((res)=>{
                console.log("Call GetRecentlyPlayed API successed!")
                let retv = res.data
                console.log(retv)
                var temp_map = {}
                for(var i=0; i<retv["items"].length; i++) {
                    var track_name = retv["items"][i]["track"]["name"]
                    var track_id = retv["items"][i]["track"]["id"]

                    if(!(track_name in temp_map)) {
                        this.recently_played.push([track_name, track_id])
                        temp_map[track_name] = 0
                    }
                }
            })
        },
        WrapGetFollowedArtist() {
            // 獲取使用者追隨的藝人
            return GetFollowedArtist(this.$store.access_token).then((res)=>{
                console.log("Call GetFollowedArtist API successed!")
                let retv = res.data
                var artist_lst = retv['artists']['items']

                if(artist_lst.length>0) {
                    for(var i=0; i<artist_lst.length; i++) {
                        var artist_name = artist_lst[i]["name"]
                        var artist_id = artist_lst[i]["id"]
                        this.followed_artist.push([artist_name, artist_id])

                        var artist_genres = artist_lst[i]["genres"]
                        // 若此artist有genre list的話，則循環加入genre_dict["artist"]來計次
                        if(artist_genres.length>0) {
                            for(var j=0; j<artist_genres.length; j++) {
                                // 若此genre已存在於genre_dict["artist"]，則計次+1
                                // 否則新建一組key-value表示genre-frequency
                                if(artist_genres[j] in this.genre_dict["artist"]) {
                                    this.genre_dict["artist"][artist_genres[j]]+=1
                                } else {
                                    this.genre_dict["artist"][artist_genres[j]]=1
                                }
                            }
                        }
                    }
                }
            })
        },
        send_tags(obj) {
            var send_obj = {
                'Genres':[],
                'Artists': [],
                'Tracks': []
            }
            var tags_lst = obj['tags_lst']
            for(var i=0; i<tags_lst.length; i++) {
                for(var j=0; j<this.tags_data.length;j++) {
                    if(this.tags_data[j]['tags'].includes(tags_lst[i])) {
                        if(j==0) {
                            send_obj[this.tags_data[j]['class']].push(tags_lst[i])
                        } else if(j==1) {
                            for(var k=0; k<this.followed_artist.length; k++) {
                                if(this.followed_artist[k][0]==tags_lst[i]) {
                                    send_obj[this.tags_data[j]['class']].push(this.followed_artist[k][1])
                                }
                            }
                            
                        } else if(j==2) {
                            for(k=0; k<this.recently_played.length; k++) {
                                if(this.recently_played[k][0]==tags_lst[i]) {
                                    send_obj[this.tags_data[j]['class']].push(this.recently_played[k][1])
                                }
                            }
                            
                        }
                    }
                }
            }
            // console.log(send_obj)

            var t = JSON.stringify(send_obj)
            this.$router.push({
                name: 'song_list', 
                query: {
                    list_type: 1,
                    tags_obj: t
                },
            })
        }
    },
}
</script>

<style scoped>
#bg {
    width: 100%;
    height: 100%;
    background: linear-gradient(180deg, #72BFE6 0%, #46277A 100%);
    background-size: cover;
    position: fixed;
    margin: 0;
    top: 0px;
	left: 0px;
    z-index: -100;
}


#tagTable_container {
    margin-left: 15%;
    width: 70%
}
</style>



