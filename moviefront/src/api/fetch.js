import api from './index';
import axios from '../http';
import qs from 'qs' ;



axios.defaults.withCredentials = true // 若跨域请求需要带 cookie 身份识别
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'

const headers = {
  // 'Content-Type': 'application/json;charset=utf-8',
    'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
  // 'Access-Control-Allow-Origin':'*',
  "Access-Control-Allow-Credentials": "true",
  'Access-Control-Allow-Methods':'PUT,POST,GET,DELETE,OPTIONS',
  // "Access-Control-Request-Headers": 'Origin,Access-Control-Request-Headers,Access-Control-Allow-Headers,DNT,X-Requested-With,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Accept,Connection,Cookie,X-XSRF-TOKEN,X-CSRF-TOKEN,Authorization',
  // 这里有一个很玄学的问题
  token: localStorage.getItem('token'),
};
export default {
  getPerson(num) {
    return axios.get(api.getPerson(), { params: { page: num, size: 9 } }, { headers });
  },
  getMovie() {
    return axios.get(api.getMovie(), { params: { size: 12 } }, { headers });
  },
  getRecommend(info) {
    // const info = localStorage.getItem('user_pk');
    // console.log(info.userId)
    return axios.get(api.getRecommend(),{params:{user_md5:info.userId}}, {headers});
  },
  getMovieHigh() {
    return axios.get(api.getMovieHigh(),{ params: {}},{ headers });
  },
  getMovieList(info) {
    return axios.get(api.getMovieByTag(), { params: {tags:info.tags,page:info.page,size:info.size} }, { headers });
  },
  getMovieInfo(id) {
    return axios.get(api.getMovieInfo(), { params: { movieId: id } }, { headers });
  },
  putMovie(info) {
    // headers.token = localStorage.getItem('token');
    return axios.get(api.putMovie(), { params: {user_md5:info.userId,movie_id:info.movieId,rating:info.rating}}, { headers });
  },

  userRegister(info) {
    return axios.get(api.userRegister(), { params: {password:info.password,username:info.username} }, { headers });
  },
  movieTags() {
    return axios.get(api.getMovieTag(), { headers });
  },
  userLogin(info) {
    // return axios.post(api.userLogin(), JSON.stringify(info), { headers });
    return axios.get(api.userLogin(), { params: {password:info.password,username:info.username} }, { headers });

  },


  logout() {
    headers.token = localStorage.getItem('token');
    // my_token = localStorage.getItem('token');
    return axios.get(api.logout(), null, { headers });
  },


};
