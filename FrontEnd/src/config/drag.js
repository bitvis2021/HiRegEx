import Vue from 'vue';
const drag = Vue.directive('drag', {
    bind: function (el) { },
    inserted: function (el) {
        el.onmousedown = function (e) {
            var disx = e.pageX - el.offsetLeft;
            var disy = e.pageY - el.offsetTop;
            document.onmousemove = function (e) {
                el.style.left = e.pageX - disx + 'px';
                el.style.top = e.pageY - disy + 'px';
            }
            document.onmouseup = function () {
                document.onmousemove = document.onmouseup = null;
            }
        }
    },
    updated: function (el) { }
})
export default drag;

