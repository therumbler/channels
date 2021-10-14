(function () {
    let ws = null;
    const $ = document.querySelector.bind(document);
    //const BASE_URL = window.location.hostname == 'tv.freeshows.site' ? '.' : 'https://tv.freeshows.site';
    const BASE_URL = '.';

    function initWebsocket(){
        var wsUrl = window.location.protocol === 'https:' ? 'wss://' : 'ws://'
	wsUrl = wsUrl + window.location.host + '/ws/';
        ws = new WebSocket(wsUrl); 
	ws.onopen = function (evt) {
	    console.log('websocket opened');
	}
	ws.onmessage = function(msg){
	    console.log('msg in', msg);
        }
    }
    async function fetchVideo(channel) {
        console.log(`fetchVideo: ${channel} `);
        let r = await fetch(`${BASE_URL}/api/streams/${channel}`);
        let resp;
        try {
            resp = await r.json();
        } catch {
            $("#message").innerText = "server error";
            return;
        }
        console.log(resp);
        window.localStorage.setItem("channel", channel);
        return resp;
    }

    async function fetchLineup() {
        let r = await fetch(`${BASE_URL}/api/lineup`);
        return await r.json();
    }

    function createVideoElement(videoObj) {
        console.log('createVideoElement');
        let element = document.createElement('video');
        // element.setAttribute('poster', videoObj.image);
        element.setAttribute('controls', true);
        element.setAttribute('class', "video-js");
        element.setAttribute('data-setup', '{"fluid": true}');
        let source = document.createElement('source');
        source.setAttribute('src', videoObj.stream_url);
        element.appendChild(source);

        return element;
    }

    function createVideo(videoObj) {
        let element = document.createElement('div');
        let h2 = document.createElement('h2');
        h2.innerText = videoObj.title;
        element.appendChild(h2);
        let h3 = document.createElement("h3");
        if (videoObj.listing.length > 0) {
            h3.innerText = videoObj.listing[0].events[0].program.title;
        }

        element.appendChild(h3);

        let videoElement = createVideoElement(videoObj);
        element.appendChild(videoElement);
        return element;
    }
    function renderVideo(videoObj) {
        console.log('renderVideo');

        let element = createVideo(videoObj);

        $('#video').appendChild(element);
        videojs($("video"));
    }

    async function startStream(channel) {
        $("#message").innerText = `loading ${channel}...`;
        let videoObj = await fetchVideo(channel);
        renderVideo(videoObj);
        $("#message").innerText = "";
    }

    async function videoChange(evt) {
        let videoId = evt.target.value;
        startStream(videoId);
    }

    async function stopStream(channel) {
        let r = await fetch(`${BASE_URL}./api/streams/${channel}`, { 'method': 'DELETE' });
        let resp = await r.json();
        console.log(resp);
        window.localStorage.removeItem("channel");
        return resp;
    }

    async function beforeUnload(evt) {
        console.error('beforeUnload');
        let channel = localStorage.getItem("channel");
        if (channel) {
            await stopStream(channel);
        }
    }

    function renderChannel(channel) {
        let element = document.createElement('span');
        element.setAttribute("class", "item");
        let anchor = document.createElement('a');
        anchor.setAttribute('href', `./?channel=${channel.GuideNumber}`);
        let title = document.createElement('span');
        title.innerText = channel.GuideName;
        let img;
        if (channel.listing.length > 0) {
            let event = channel.listing[0].events[0];
            let channelDescription = `${event.program.title} on ${channel.listing[0].affiliateName}`;
            anchor.setAttribute("title", channelDescription)
            title.innerText = title.innerText + ` - (${event.program.title})`
            img = document.createElement('img');
            img.setAttribute('src', `https://zap2it.tmsimg.com/assets/${event.thumbnail}.jpg?w=400`);
        }
        if (img) {
            anchor.appendChild(img);
        } else {
            anchor.appendChild(title);
        }
        element.appendChild(anchor);
        $('#channels').appendChild(element);
    }

    function renderLineup(lineup) {
        console.log('renderLineup');
        Array.prototype.forEach.call(lineup, function (channel, i) {
            renderChannel(channel);
        });
    }

    async function displayLineup() {
        let lineup = await fetchLineup();
        renderLineup(lineup);
    }

    async function init() {
	initWebsocket();
        window.addEventListener('beforeunload', beforeUnload);
        const urlParams = new URLSearchParams(window.location.search);
        const channel = urlParams.get('channel');

        if (channel) {
            startStream(channel);
        } else {
            await displayLineup();
            console.error("no channel id passed in")
        }
    }

    init();
})();
