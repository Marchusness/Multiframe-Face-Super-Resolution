import * as THREE from 'three';
import { FaceMask } from './face_mask';
import { VideoBackground } from './video_bg';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

/**
 * 
 * Finds distance to position perspective camera
 * 
 * @param {Number} height height of video 
 * @param {Number} fov fov of perspective camera
 */
const cameraDistance = (height, fov) => {
  return (height / 2) / Math.tan((fov/2) * Math.PI / 180);
}

/**
 * 
 * Call these methods.
 * 
 * 1) animate inside request animation frame
 * 2) resize inside request animation frame
 * 3) onLandmarks on recieving new face landmarks
 * 
 */
export class SceneManager {
  constructor(canvas, debug=false, useOrtho=true) {
    this.canvas = canvas;
    this.scene = new THREE.Scene();
    this.debug = debug;
    this.useOrtho = useOrtho;
    this.renderer = new THREE.WebGLRenderer({
      preserveDrawingBuffer: true,
      canvas: this.canvas,
      devicePixelRation: window.devicePixelRatio || 1
    });
    this.fov = 63;
    this.buildCamera();
    this.buildControls();
    this.buildVideoBg();
    this.buildFaceMask();
  }

  buildVideoBg() {
    // video background for canvas
    this.videoBg = new VideoBackground(this.scene, 
      this.videoWidth, 
      this.videoHeight
    );
  }

  buildFaceMask() {
    // this component draws faces
    this.faceMask = new FaceMask(this.scene, 
      this.videoWidth, 
      this.videoHeight
    )
  }

  buildControls() {
    if (this.debug) {
      this.controls = new OrbitControls(
        this.camera, this.renderer.domElement 
      );
      this.controls.update();
    }
  }

  buildCamera() {
    this.useOrtho ? this.buildOrthoCamera() : this.buildPerspectiveCamera();
  }

  buildOrthoCamera() {
    this.camera = new THREE.OrthographicCamera(
      - this.videoWidth / 2,
      this.videoWidth / 2,
      this.RendererHeight / 2,
      - this.RendererHeight / 2,
      -2000, 
      2000
    )
    this.camera.position.z = 1
  }

  buildPerspectiveCamera() {

    this.camera = new THREE.PerspectiveCamera(
      this.fov,
      this.renderer.domElement.width / this.RendererHeight,
      1.0, // near
      10000, // far
    )

    this.camera.position.z = cameraDistance(
      this.RendererHeight, 
      this.fov
    ); 
  }

  // we need to resize canvas rendering dimensions
  // when canvas sytling dimensions change
  resizeRendererToDisplaySize() {

    const canvas = this.renderer.domElement;

    // match dimension of canvas with
    // dimension of video
    if (this.videoWidth != canvas.clientWidth
      || this.RendererHeight != canvas.clientHeight) {
      canvas.style.width =  `${this.videoWidth}px`;
      canvas.style.height = `${this.RendererHeight}px`;
      // canvas.style.background = `red`;
    }

    // canvas has 2 width
    // 1) style width set with style attribute
    // 2) rendering width set with width and height attribute
    // update rendering width to match styling width.
    const width  = canvas.clientWidth | 0;
    const height = canvas.clientHeight | 0;
    const needResize = canvas.width !== width || canvas.height !== height;
    if (needResize) {
      this.renderer.setSize(width, height, false);
    }
    return needResize;
  }

  updateCamera() {
    // camera need to be adjusted according to
    // renderer dimensions
    this.camera.aspect = this.videoWidth / this.RendererHeight;
    if (this.camera.type == 'OrthographicCamera') {
      this.camera.top = this.RendererHeight / 2
      this.camera.bottom = -this.RendererHeight / 2
      this.camera.left = -this.videoWidth / 2
      this.camera.right = this.videoWidth / 2  
    } else {
      this.camera.position.z = cameraDistance(this.RendererHeight, this.fov);
    }
    this.camera.updateProjectionMatrix();
  }

  animate() {
    if (this.controls) {
      this.controls.update();
    }

    if (this.resizeRendererToDisplaySize()) {
      
      // facemask needs to scale faces according to 
      // renderer dimensions
      this.faceMask.updateDimensions(
        this.videoWidth, 
        this.videoHeight
      );


      // update video width and height
      this.videoBg.updateDimensions(
        this.videoWidth, 
        this.videoHeight
      );

      this.updateCamera();
    }


    // update video background
    this.videoBg.update();

    // update faces mask
    this.faceMask.update();

    // render scene
    this.renderer.render(this.scene, this.camera);
  }

  resize(videoWidth, videoHeight) {
    if (this.videoWidth != videoWidth) {
      this.videoWidth = videoWidth;
      this.videoHeight = videoHeight;
      this.RendererHeight = videoHeight*2;
      this.animate();
    }
    
  }

  onLandmarks(image, landmarks) {
    if (image && landmarks) {
      this.videoBg.setImage(image);
      this.faceMask.updateLandmarks(landmarks);
    }
  }
}