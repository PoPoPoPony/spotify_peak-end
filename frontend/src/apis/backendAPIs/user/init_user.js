import request from '../../../utils/requestBackend'


export function InitUser(id, email, between, within) {
    let data = JSON.stringify({
        'userID': id,
        'userEmail': email,
        'betweenType': between,
        'withinType': within,
    })

    let config = {
        url: '/user/initUser',
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        data: data
    }
    

    return request(config)
}