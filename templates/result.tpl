<!-- ここでbase.tplを利用することを宣言 -->
% rebase('templates/base.tpl', use_bokeh=True)
<div>
  <!-- 変数を利用 -->
  <h3>アワビの特徴は、性別{{ abalone.sex_str }}、殻長{{ abalone.length }}mm、殻幅{{ abalone.diameter }}mm、高さ{{ abalone.height }}mm、重さ{{ abalone.weight }}グラムですね</h3>
  <h3>このアワビの推定年齢は{{ abalone.age }}歳です</h3>
</div>
<div>
  {{ !graph }}
</div>