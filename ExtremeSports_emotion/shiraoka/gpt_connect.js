function gpt_connect() {
  const netaTitle = args[0]; // 一番目はネタのタイトル
  const chatList = args.slice(1); // それ以降はチャットの履歴

  return new Promise((resolve, reject) => {
    var headers = {
      'Content-Type': 'application/json',
      Authorization: 'Bearer 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',
    };

    var messages = [
      {
        'role': 'system', 'content': '漫才のボケを担当',
      },
      {      'role': 'user', 'content':
      `
      ＃概要
      あなたはソフトバンクのロボット、ペッパー君の内部AIです。
      あなたがボケた後に私がツッコミしますので続けてください。

      ボケをする際には以下の制約を守ってください。
      ＃制約
        1. 私がツッコミしやすいように簡潔なボケであること
        2. 文字数は30文字以内
        3. 自分のボケだけを出力
        4. 私が「もうええわ」と言ったら「ありがとうございました」と言って終わる

      では始めます。
      ショートコント「${netaTitle}」
      `
    }
  ]
  var resultChatList = chatList.map(inputString => {
    const [role, content] = inputString.split('@');
    return {
      'role': role,
      'content': content
    };
  });

  const raw = JSON.stringify({
    model: 'gpt-3.5-turbo',
    messages: messages.concat(resultChatList),
    temperature: 0.0,
  });

  const options = {
    url: 'https://api.openai.com/v1/chat/completions',
    method: 'POST',
    headers: headers,
    body: raw,
    redirect: 'follow',
  };

  request(options, function (error, response, body) {
    var obj = JSON.parse(response.body);
    resolve(obj.choices[0].message['role'] + "@" + obj.choices[0].message['content']);
  });
})
}
