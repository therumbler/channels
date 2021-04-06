(function () {
    const $ = document.querySelector.bind(document);

    async function fetchVideo(channel) {
        console.log(`fetchVideo: ${channel} `)
        let r = await fetch(`./api/streams/${channel}`)
        let resp = await r.json();
        console.log(resp);
        window.localStorage.setItem("channel", channel)
        return resp;
    }

    async function fetchLineup() {
        let r = await fetch("./api/lineup")
        return await r.json();
    }

    function createVideoElement(videoObj) {
        console.log('createVideoElement')
        let element = document.createElement('video');
        // element.setAttribute('poster', videoObj.image);
        element.setAttribute('controls', true);
        element.setAttribute('class', "video-js");
        element.setAttribute('data-setup', '{"fluid": true}');
        let source = document.createElement('source')
        source.setAttribute('src', videoObj.stream_url);
        element.appendChild(source);

        return element;
    }

    function createVideo(videoObj) {
        let element = document.createElement('div')
        let h2 = document.createElement('h2')
        h2.innerText = videoObj.title;
        element.appendChild(h2);
        let h3 = document.createElement("h3");
        h3.innerText = videoObj.listing[0].events[0].program.title;
        element.appendChild(h3);

        let videoElement = createVideoElement(videoObj);
        element.appendChild(videoElement);
        return element
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
        $("#message").innerText = "";
        renderVideo(videoObj);
    }

    async function videoChange(evt) {
        let videoId = evt.target.value;
        startStream(videoId);
    }
    async function stopStream(channel) {
        let r = await fetch(`./api/streams/${channel}`, { 'method': 'DELETE' })
        let resp = await r.json();
        console.log(resp);
        window.localStorage.removeItem("channel");
        return resp;
    }

    async function beforeUnload(evt) {
        console.error('beforeUnload')
        let channel = localStorage.getItem("channel");
        if (channel) {
            await stopStream(channel)
        }
    }

    function renderChannel(channel) {
        let div = document.createElement('div');
        let anchor = document.createElement('a');
        anchor.setAttribute('href', `./?channel=${channel.GuideNumber}`);

        let h2 = document.createElement('h2');
        anchor.appendChild(h2);
        h2.innerText = channel.GuideName

        if (channel.listing.length > 0) {
            h2.innerText = h2.innerText + ` - (${channel.listing[0].events[0].program.title})`
        }
        div.appendChild(anchor);
        $('#channels').appendChild(div);
    }
    function renderLineup(lineup) {
        console.log('renderLineup');
        Array.prototype.forEach.call(lineup, function (channel, i) {
            // console.log(channel);
            renderChannel(channel);
        });
    }
    async function displayLineup() {
        let lineup = await fetchLineup();
        renderLineup(lineup);
    }
    async function init() {
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
