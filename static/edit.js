document.addEventListener("input", function(ev) {
  if("textarea" === ev.target.tagName.toLowerCase()) {
    elem = ev.target
    elem.style.height = "inherit"
    computed = window.getComputedStyle(elem)
    const h = (parseInt(computed.getPropertyValue("border-top-width"), 10) +
               parseInt(computed.getPropertyValue("padding-top"), 10) +
               elem.scrollHeight +
               parseInt(computed.getPropertyValue("padding-bottom"), 10) +
               parseInt(computed.getPropertyValue("border-bottom-width"), 10))
    elem.style.height = h + "px"
  }
}, false)

