export async function clipboardCopy(text) {
  try {
    if (navigator.clipboard) {
      await navigator.clipboard.writeText(text)
      return true
    }
    fallbackCopy(text)
    return true
  } catch (e) {
    return false
  }
}

function fallbackCopy(text) {
  const textArea = document.createElement('textarea')
  textArea.value = text
  textArea.style.top = '0'
  textArea.style.left = '0'
  textArea.style.position = 'fixed'

  document.body.appendChild(textArea)
  textArea.focus()
  textArea.select()

  document.execCommand('copy')
  document.body.removeChild(textArea)
}
