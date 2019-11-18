export const rtrim = /^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g;
export function trim( text ) {
  return text == null ?
    "" :
    ( text + "" ).replace( rtrim, "" );
};

export function getCookie(name) {
  let cookieValue = null;

  if (document.cookie && document.cookie !== '') {
    let cookies = document.cookie.split(';');

    for (let i = 0; i < cookies.length; i++) {
      let cookie = trim(cookies[i]);

      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }

  return cookieValue;
}
export function setCookie(name, value){
  document.cookie = `${name}=${value};`
}
export function deleteCookie(name){
  document.cookie = `${name}=;`
}