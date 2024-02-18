/**
 * This function will return you boolean value if the DOM element is overflowed
 *
 * @param element
 * @returns {boolean}
 */
function isOverflown(element) {
    return element.scrollHeight > element.clientHeight || element.scrollWidth > element.clientWidth;
}
