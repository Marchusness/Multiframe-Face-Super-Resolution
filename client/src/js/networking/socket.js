

export class Socket {
    constructor(url="ws://localhost:8001/") {
        this.websocket = new WebSocket(url);
    }

    sendCanvas(canvas){
        var img_base64 = canvas.toDataURL('image/jpeg').replace(/^.*,/, '')
        this.websocket.send(img_base64)
    }

}

// const event = {type: "play", column: 3};

// websocket.send(JSON.stringify(event));

// function sendMoves(board, websocket) {
//     // When clicking a column, send a "play" event for a move in that column.
//     board.addEventListener("click", ({ target }) => {
//       const column = target.dataset.column;
//       // Ignore clicks outside a column.
//       if (column === undefined) {
//         return;
//       }
//       const event = {
//         type: "play",
//         column: parseInt(column, 10),
//       };
//       websocket.send(JSON.stringify(event));
//     });
//   }


//   websocket.addEventListener("message", ({ data }) => {
//     const event = JSON.parse(data);
//     // do something with event
//   });

//   function showMessage(message) {
//     window.setTimeout(() => window.alert(message), 50);
//   }
  
//   function receiveMoves(board, websocket) {
//     websocket.addEventListener("message", ({ data }) => {
//       const event = JSON.parse(data);
//       switch (event.type) {
//         case "play":
//           // Update the UI with the move.
//           playMove(board, event.player, event.column, event.row);
//           break;
//         case "win":
//           showMessage(`Player ${event.player} wins!`);
//           // No further messages are expected; close the WebSocket connection.
//           websocket.close(1000);
//           break;
//         case "error":
//           showMessage(event.message);
//           break;
//         default:
//           throw new Error(`Unsupported event type: ${event.type}.`);
//       }
//     });
//   }

//   socket.addEventListener('message', (e) => {
//     let ctx = msg.getContext("2d");
//     let image = new Image();
//     image.src = URL.createObjectURL(e.data);
//     image.addEventListener("load", (e) => {
//         ctx.drawImage(image, 0, 0, msg.width, msg.height);
//     });
// });