import "./styles.css";
import { PUBLIC_PATH } from './js/public_path';
import { VideoFrameProvider } from './js/video_frame_provider';
import { CameraFrameProvider } from './js/camera_frame_provider';
import { FacemeshLandmarksProvider } from './js/facemesh/landmarks_provider';
import { SceneManager } from "./js/three_components/scene_manager";
import { Socket } from "./js/networking/socket";

const template = `
<div class="video-container">
  <span class="loader">
    Loading ...
  </span>
  <div>
    <video class="input_video" controls playsinline>
    </video>
  </div>
  <div>
    <h2>Output Canvas</h2>
    <canvas class="output_canvas"></canvas>
  </div>
</div>
`;

document.querySelector("#app").innerHTML = template;

async function main() {

  document.querySelector(".video-container").classList.add("loading");

  const video = document.querySelector('.input_video');
  const canvas = document.querySelector('.output_canvas');

  const useOrtho = true;
  const debug = false;

  let socket;
  let sceneManager;
  let facemeshLandmarksProvider;
  let videoFrameProvider;

  const onLandmarks = ({image, landmarks}) => {
    socket.sendCanvas(canvas);
    sceneManager.onLandmarks(image, landmarks);
  }

  const onFrame = async (video) => {
    
    // console.log(video.videoWidth, video.videoHeight);
    sceneManager.resize(video.videoWidth/video.videoHeight * 512, 512);
    // sceneManager.resize(video.videoWidth*10, video.videoHeight*10);
    try {
      await facemeshLandmarksProvider.send(video);
    } catch (e) {
      alert("Not Supported on your device")
      console.error(e);
      videoFrameProvider.stop();      
    }
  }

  function animate () {
    requestAnimationFrame(animate);
    // sceneManager.resize(video.clientWidth, video.clientHeight);
    // console.log(video.clientWidth, video.clientHeight);
    sceneManager.animate();
  }

  socket = new Socket();
  sceneManager = new SceneManager(canvas, debug, useOrtho);
  facemeshLandmarksProvider = new FacemeshLandmarksProvider(onLandmarks);
  if (true){
    videoFrameProvider = new CameraFrameProvider(video, onFrame);
  } else {
    video.innerHTML = `<source  src="${PUBLIC_PATH}/assets/videos/thief.mov">`
    video.autoplay=true;
    videoFrameProvider = new VideoFrameProvider(video, onFrame)
  }
  
  await facemeshLandmarksProvider.initialize();
  videoFrameProvider.start();

  animate();

  document.querySelector(".video-container").classList.remove("loading");
}

main();
