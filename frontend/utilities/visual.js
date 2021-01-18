export function getViewportSize() {
  const scale = window.visualViewport?.scale
  if (scale) {
    return {
      width: window.visualViewport.width * scale,
      height: window.visualViewport.height * scale,
    }
  }
  return {
    width: window.innerWidth,
    height: window.innerHeight,
  }
}
