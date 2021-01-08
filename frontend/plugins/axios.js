export default function ({ $axios }) {
  $axios.defaults.xsrfCookieName = 'csrftoken'
  $axios.defaults.xsrfHeaderName = 'X-CSRFToken'
}
