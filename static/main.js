(function(){
    console.log('main.js')

    const $ = document.querySelector.bind(document);


    async function fetchVideo(channel){
        console.log(`fetchVideo: ${channel} `)
        let r = await fetch(`./api/channels/${channel}`)
        let resp = await r.json();
        console.log(resp);
        window.localStorage.setItem(channel,true)
        return resp;
    }
    function createVideoElement(videoObj){
        console.log('createVideoElement')
        let element = document.createElement('video');
        // element.setAttribute('poster', videoObj.image);
        element.setAttribute('controls', true);
        element.setAttribute('class', "video-js");
        element.setAttribute('data-setup','{"fluid": true}');
        let source = document.createElement('source')
        source.setAttribute('src', videoObj.stream_url);
        element.appendChild(source);

        return element;
    }

    function createVideo(videoObj){
        
        let element = document.createElement('div')
        let h2 = document.createElement('h2')
        h2.innerText = videoObj.title;
        element.appendChild(h2);
        
        let videoElement = createVideoElement(videoObj);
        element.appendChild(videoElement);
        return element
    }
    function renderVideo(videoObj){
        console.log('renderVideo');
        
        let element = createVideo(videoObj);

        $('#video').appendChild(element);
        videojs(element.children[1]);
    }

    async function showVideo(channel){
        let videoObj = await fetchVideo(channel);
        renderVideo(videoObj);
    }

    async function videoChange(evt){
        let videoId = evt.target.value;
        showVideo(videoId);
    }
    async function stopVideo(channel){
        let r = await fetch(`./api/channels/${channel}/stop`)
        let resp = await r.json();
        console.log(resp);
        window.localStorage.removeItem(channel);
        return resp;
    }

    async function beforeUnload(evt){
        console.error('beforeUnload')
        let channel = localStorage.getItem("channel");
        if(channel){
            await stopVideo(channel)
        }
    }

    async function init (){
        window.addEventListener('beforeunload', beforeUnload);
        const urlParams = new URLSearchParams(window.location.search);
        const channel = urlParams.get('channel');
        console.log(channel);
        if(channel){
            showVideo(channel);
        } else {
            console.error("no channel id passed in")
      }
        // showVideo('11775043598')
    }
    init();
})();
