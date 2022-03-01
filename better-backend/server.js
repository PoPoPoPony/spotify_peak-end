let express = require('express')
let request = require('request')

let app = express()

let redirect_uri =
  process.env.REDIRECT_URI ||
  'http://localhost:8888/callback'

// 需要先設置環境變數
// npm start

let redirect_page = "0"
let between_subject_type="0"
let within_subject_type="0"

app.get('/login', function (req, res) {
  let params = new URLSearchParams([
    ['response_type', 'code'],
    ['client_id', process.env.SPOTIFY_CLIENT_ID],
    ['scope', 'user-read-private user-read-email user-library-read'],
    ['redirect_uri', redirect_uri]
  ]).toString()

  redirect_page=req.query.redirect_page
  between_subject_type=req.query.between_subject_type
  within_subject_type = req.query.within_subject_type

  res.redirect('https://accounts.spotify.com/authorize?' + params)
}) 

app.get('/callback', function (req, res) {
  let code = req.query.code || null
  let authOptions = {
    url: 'https://accounts.spotify.com/api/token',
    form: {
      code: code,
      redirect_uri,
      grant_type: 'authorization_code'
    },
    headers: {
      'Authorization': 'Basic ' + (new Buffer.from(
        process.env.SPOTIFY_CLIENT_ID + ':' + process.env.SPOTIFY_CLIENT_SECRET
      ).toString('base64'))
    },
    json: true
  }
  request.post(authOptions, function (error, response, body) {
    var access_token = body.access_token
    let uri = ''
    if(redirect_page=="0") {
      uri = 'http://localhost:8080/create_list'
    } else {
      uri = 'http://localhost:8080/tags'
    }
    params ="?access_token=" + access_token + "&between_subject_type=" + between_subject_type + "&within_subject_type=" + within_subject_type

    res.redirect(uri + params)
  })
})

let port = process.env.PORT || 8888
console.log(`Listening on port ${port}. Go /login to initiate authentication flow.`)
app.listen(port)