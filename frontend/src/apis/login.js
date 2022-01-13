import request from '../utils/request'


export function Login() {
    let config = {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        url: '/login',
        method: 'GET',
        
    }

    return request(config)
}

export async function getToken() {
    // var url = new URL("https://accounts.spotify.com/authorize?")
    // var params={
    //         client_id: '5e3c611726d54d488fb918a4c8a8739c',
    //         response_type: 'code',
    //         redirect_uri: 'http://localhost:8080',
    //         show_dialog:true,
    // }
    // url.setRequestProperty("Content-Type", "application/x-www-form-urlencoded")
    // url.search = new URLSearchParams(params).toString()
    // const result = await fetch(url)
    // const data = await result.json();
    // return data

    // let config = {
    //     url: 'https://accounts.spotify.com/authorize',
    //     method: 'GET',
    //     headers: { "Content-Type": "application/x-www-form-urlencoded" },
    //     params: {
    //         client_id: '5e3c611726d54d488fb918a4c8a8739c',
    //         response_type: 'code',
    //         redirect_uri: 'http://localhost:8080',
    //         show_dialog:true,
    //     },
    //     responseType: 'text'
    // }

    // return request(config)



    // const result = await fetch("https://accounts.spotify.com/authorize?", {
    //     method: "POST",
    //     headers: {
    //         "Content-Type": "application/x-www-form-urlencoded",
    //         Authorization: "Basic " + window.btoa(clientId + ":" + clientSecret),
    //     },
    //     body: "grant_type=client_credentials",
    // });

    // const data = await result.json();
    // return data.access_token;
}







export async function getCategories(token) {
    const result = await fetch(
        `https://api.spotify.com/v1/browse/categories`,
        {
            method: "GET",
            headers: { Authorization: "Bearer " + token },
        }
    );
    const data = await result.json();
    return data.categories.items;
}

// export async function getCategories(token) {
//     const result = await fetch(
//         `https://api.spotify.com/v1/browse/categories`,
//         {
//             method: "GET",
//             headers: { Authorization: "Bearer " + token },
//         }
//     );
//     const data = await result.json();
//     return data.categories.items;
// }
