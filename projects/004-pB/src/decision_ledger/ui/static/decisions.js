/**
 * decisions.js — T008
 * 结论: 决策表单交互 JS（键盘快捷键 1-4、Enter 提交、字数倒计时、commit 按钮 gate）
 * 细节:
 *   - 数字键 1-4 快速选择 action radio
 *   - Enter 键提交当前焦点所在表单
 *   - updateCount(textarea): 实时字数倒计时
 *   - checkWouldHaveActed(): commit 按钮在 would_have_acted 未选前保持 disabled
 */

'use strict';

/**
 * 实时更新 textarea 字数计数
 * @param {HTMLTextAreaElement} el
 */
function updateCount(el) {
  const max = parseInt(el.getAttribute('maxlength') || '80', 10);
  const current = el.value.length;
  const countEl = document.getElementById('reason-count');
  if (countEl) {
    countEl.textContent = current + '/' + max;
    if (current >= max) {
      countEl.style.color = 'var(--pico-color-red-500, #e74c3c)';
    } else {
      countEl.style.color = '';
    }
  }
}

/**
 * 检查 would_have_acted_without_agent 是否已选中，控制 commit button
 */
function checkWouldHaveActed() {
  const btn = document.getElementById('commit-btn');
  if (!btn) return;

  const radios = document.querySelectorAll('input[name="would_have_acted_without_agent"]');
  let anyChecked = false;
  radios.forEach(function(r) {
    if (r.checked) anyChecked = true;
  });
  btn.disabled = !anyChecked;
}

// 键盘快捷键 1-4 → action radio
document.addEventListener('keydown', function(e) {
  // 如果焦点在输入框/textarea 内，不拦截
  const tag = document.activeElement && document.activeElement.tagName.toLowerCase();
  if (tag === 'input' || tag === 'textarea' || tag === 'select') return;

  const keyMap = {
    '1': 'buy',
    '2': 'sell',
    '3': 'hold',
    '4': 'wait',
  };

  if (keyMap[e.key]) {
    const actionValue = keyMap[e.key];
    // intended_action 或 final_action
    const radio = document.querySelector(
      'input[name="intended_action"][value="' + actionValue + '"],' +
      'input[name="final_action"][value="' + actionValue + '"]'
    );
    if (radio) {
      radio.checked = true;
      radio.dispatchEvent(new Event('change', { bubbles: true }));
    }
  }
});
