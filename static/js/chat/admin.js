var pusherChat = (function() {
  // pusherのAPI設定
  var pusher = new Pusher("768af5bb1417be83adc3", {
    authEndpoint: "/chats/pusher/auth/",
    cluster: "ap3",
    encrypted: true
  });

  // チャットのデフォルト設定
  let chat = {
    messages: [],
    currentRoom: "",
    currentChannel: "",
    subscribedChannels: [],
    subscribedUsers: []
  };

  // 一般チャンネルにsubscribeする
  var generalChannel = pusher.subscribe("general-channel");

  // DOMの取得
  const chatBody = $(document);
  const chatRoomsList = $("#rooms");
  const chatReplyMessage = $("#replyMessage");

  // UIを操作するオブジェクトの定義
  const helpers = {
    // チャットメッセージUIをクリアする
    clearChatMessages: () => $("#chat-msgs").html(""),

    // 新しいメッセージを表示する
    displayChatMessage: message => {
      if (message.email === chat.currentRoom) {
        if (message.sender === "Support") {
          $("#chat-msgs").prepend(
            `<tr class="bg-yellow-100">
                <td>
                    <div class="font-semibold">${message.sender} <span class="date">${message.createdAt}</span></div>
                    <div class="message">${message.text}</div>
                </td>
            </tr>`
          );
        } else {
          $("#chat-msgs").prepend(
            `<tr class="bg-blue-100">
                <td>
                    <div class="font-semibold">${message.sender} <span class="date">${message.createdAt}</span></div>
                    <div class="message">${message.text}</div>
                </td>
            </tr>`
          );
        }
      }
    },

    // 新しいチャットルームをロードする
    loadChatRoom: evt => {
      chat.currentRoom = evt.target.dataset.roomId;
      chat.currentChannel = evt.target.dataset.channelId;

      if (chat.currentRoom !== undefined) {
        $(".response").show();
        $("#room-title").text(evt.target.dataset.roomId);
      }

      evt.preventDefault();
      helpers.clearChatMessages();
    },

    // 返事する
    replyMessage: evt => {
      evt.preventDefault();

      let createdAt = new Date();
      createdAt = createdAt.toLocaleString();

      const message = $("#replyMessage input")
        .val()
        .trim();

      chat.subscribedChannels[chat.currentChannel].trigger(
        "client-support-new-message",
        {
          name: "Admin",
          email: chat.currentRoom,
          text: message,
          createdAt: createdAt
        }
      );

      helpers.displayChatMessage({
        email: chat.currentRoom,
        sender: "Support",
        text: message,
        createdAt: createdAt
      });

      $("#replyMessage input").val("");
    }
  };

  // 新しいゲストの情報を取得し、チャットに新しく設定する
  generalChannel.bind("new-guest-details", function(data) {
    chat.subscribedChannels.push(pusher.subscribe("private-" + data.email));
    chat.subscribedUsers.push(data);

    // チャットしようとしているチャットルームをリスト式で表示する
    $("#rooms").html("");
    chat.subscribedUsers.forEach(function(user, index) {
      $("#rooms").append(
        `<li class="p-5 text-center rounded bg-white mb-2 shadow"><a data-room-id="${user.email}" data-channel-id="${index}" class="nav-link" href="#">${user.email}</a></li>`
      );
    });
  });

  // ゲストから新しいメッセージのイベントを検知し、表示する
  pusher.bind("client-guest-new-message", function(data) {
    helpers.displayChatMessage(data);
  });

  // イベントリスナーの設定
  chatReplyMessage.on("submit", helpers.replyMessage);
  chatRoomsList.on("click", "li", helpers.loadChatRoom);
})();
