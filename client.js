const RawIPC = require("node-ipc");
const socket_name = "/tmp/fridge.socket"
let ipc = new RawIPC.IPC();

ipc = RawIPC;

ipc.connectTo(
    'fridge',
    socket_name,
    function(){
        ipc.of.fridge.emit('message', 'CHEGOU NO NODE')

        ipc.of.fridge.on(
            'message',  //any event or message type your server listens for
            function(data){
                console.log('Mensagem: ', data);
            }
        );
    }
);
