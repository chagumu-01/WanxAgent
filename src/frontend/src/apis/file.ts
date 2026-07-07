import { request } from "../utils/request"

export function uploadFileAPI(data: FormData) {
  return request({
    url: '/api/v1/upload',
    method: 'POST',
    data,
    headers: {}
  })
}