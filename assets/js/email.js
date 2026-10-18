/* 邮箱保护：
   1) HTML 里不出现拼好的地址，邮箱被拆成 data-email-user / data-email-domain 两段
   2) 页面加载后才拼出 mailto 并写回可见文字
   3) 禁用 JS 时显示 "email" 二字，依然不影响阅读

   注意：模板自带的 jekyll-email-protect 插件在 GitHub Pages 上不生效
   （不在白名单，未知 filter 被静默跳过），所以用这段替代。 */

(function () {
  function assemble() {
    var nodes = document.querySelectorAll('[data-email-user][data-email-domain]');
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      var addr = el.getAttribute('data-email-user') + '\u0040' + el.getAttribute('data-email-domain');
      el.setAttribute('href', 'mailto:' + addr);
      el.textContent = addr;
      el.removeAttribute('data-email-user');
      el.removeAttribute('data-email-domain');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', assemble);
  } else {
    assemble();
  }
})();
