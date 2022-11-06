
import * as THREE from 'three';
import { PUBLIC_PATH } from '../public_path';
import { makeGeometry } from '../facemesh/landmarks_helpers';

// import { face } from '../../assets/face.png';

export class FaceMask {
  constructor(scene, width, height) {
    this.scene = scene;
    this.needsUpdate = false;
    this.landmarks = null;
    this.faces = null;
    this.width = width;
    this.height = height;
    const texture = new THREE.TextureLoader().load(require(`../../assets/map.png`))
    this.material = new THREE.MeshBasicMaterial({
      map: texture,
      // wireframe: true,
      // wireframeLinewidth: 100,
    });
  }

  updateDimensions(width, height) {
    this.width = width;
    this.height = height;
    this.needsUpdate = true;
  }

  updateLandmarks(landmarks) {
    this.landmarks = landmarks;
    this.needsUpdate = true;
  }

  updateMaterial(material) {
    this.material = material;
    this.material.needsUpdate = true;
  }

  addFaces() {
    // create faces
    let geometry = makeGeometry(this.landmarks);
    this.faces = new THREE.Mesh(geometry, this.material);
    this.faces.position.set(0, this.height/2, 0);
    this.faces.scale.set(this.width, this.height, this.width);
    this.scene.add(this.faces);
  }

  removeFaces() {
    this.scene.remove(this.faces);
  }

  update() {
    // console.log(`face width: ${this.width}, height: ${this.height}`);

    if (this.needsUpdate) {
      if (this.faces != null) {
        this.removeFaces();
      }
      if (this.landmarks != null) {
        this.addFaces();
      }
      this.needsUpdate = false;
    }
  }
}
