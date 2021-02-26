const getCookie = (name) => {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined // s if r == 2 else b тернарный оператор
};

const stringToHTML = (str) => {
	const parser = new DOMParser();
	const doc = parser.parseFromString(str, 'text/html');
	return doc.body;
};