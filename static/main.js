(function(){
    console.log('main.js')

    const $ = document.querySelector.bind(document);


    async function fetchVideo(videoId){
        console.log(`fetchVideo: ${videoId} `)
        let r = await fetch(`./api/videos/${videoId}`)
        let resp = await r.json();
        console.log(resp);
        return resp;
    }
    function createVideoElement(videoObj){
        let video = videoObj.videos[0];
        console.log('createVideoElement')
        let element = document.createElement('video');
        element.setAttribute('poster', videoObj.image);
        element.setAttribute('controls', true);
        element.setAttribute('class', "video-js");
        element.setAttribute('data-setup','{"fluid": true}');
        let source = document.createElement('source')
        source.setAttribute('src', video.video_src);
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

    async function showVideo(videoId){
        let videoObj = await fetchVideo(videoId);
        renderVideo(videoObj);
    }

    async function videoChange(evt){
        let videoId = evt.target.value;
        showVideo(videoId);
    }


    async function init (){
        // $('#videoId').addEventListener('change',videoChange);
        const urlParams = new URLSearchParams(window.location.search);
        const videoId = urlParams.get('video');
        console.log(videoId);
        showVideo(videoId);
        // showVideo('11775043598')
    }
    init();
})();
