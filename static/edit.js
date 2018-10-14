/* code taken from
 * https://gomakethings.com/automatically-expand-a-textarea-as-the-user-types-using-vanilla-javascript/
 */
var autoExpand = function (field) {
    field.style.height = 'inherit';
    computed = window.getComputedStyle(field);
    var height =
        parseInt(computed.getPropertyValue('border-top-width'), 10)
         + parseInt(computed.getPropertyValue('padding-top'), 10)
         + field.scrollHeight
         + parseInt(computed.getPropertyValue('padding-bottom'), 10)
         + parseInt(computed.getPropertyValue('border-bottom-width'), 10);

    field.style.height = height + 'px';
};

document.addEventListener('input', function (event) {
  if (event.target.tagName.toLowerCase() !== 'textarea') {
        return;
    }
    autoExpand(event.target);
}, false);
