const error_message_required = "入力してください";
const error_message_select_required = "選択してください";
const error_message_min_length = "文字以上で入力してください";
const error_message_max_length = "文字以下で入力してください";
const error_message_regex = "使用可能な文字は半角英数字,全角数字,ひらがな,カナ,漢字,半全角スペース,記号-,ー,_,:,/,!,?,~,(,) です";
const error_message_field = '<span class="input-error"></span>';

// 正規表現パターン（半角英数字,全角英数字,ひらがな,カナ,漢字,スペース,-(,）,_,ー）
const regex_input = '^[-0-9a-zA-Zァ-ヴｦ-ﾟぁ-ん一-龠０-９ 　\\(\\)\\（\\）_ー!！?？~～.:/]*$';