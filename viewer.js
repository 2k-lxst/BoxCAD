import * as THREE from "three";
import { STLLoader } from "three/addons/loaders/STLLoader.js";
import { CSS2DRenderer, CSS2DObject } from "three/addons/renderers/CSS2DRenderer.js";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { ViewHelper } from "three/addons/helpers/ViewHelper.js";
import { InfiniteGridHelper } from "./libs/InfiniteGridHelper.js";

// Initialize the pybridge
new QWebChannel(qt.webChannelTransport, function (channel) {
    window.pybridge = channel.objects.pybridge;
});

let autoFitEnabled = true;
let scene, camera, renderer, currentMesh;
let measurementGroup = new THREE.Group();

const loader = new STLLoader();

window.loader = loader;

// Toggle menu visibility
const menuButton = document.getElementById('menu-button');
const menu = document.getElementById('settings-menu');

menuButton.onclick = () => {
    const isHidden = menu.classList.toggle('hidden');

    menuButton.classList.toggle("is-open", !isHidden);
    menuButton.textContent = isHidden ? '≡' : '×';
};

// Reset camera
document.getElementById('reset-cam').onclick = () => {
    fitCameraToObject(currentMesh, 0.7);
};

// Auto-fit toggle
document.getElementById("auto-fit-view-toggle").onchange = (e) => {
    autoFitEnabled = e.target.checked;
}

// Setup the CSS2D renderer
const labelRenderer = new CSS2DRenderer();
labelRenderer.setSize(window.innerWidth, window.innerHeight);
labelRenderer.domElement.style.position = "absolute";
labelRenderer.domElement.style.top = "0px";
labelRenderer.domElement.style.pointerEvents = "none";

document.body.appendChild(labelRenderer.domElement);

function createMeasurement(start, end, labelText, offsetVector, hexColor = 0xff00ee, globalMax = 10) {
    // Use a non-linear scaleFactor
    const scaleFactor = 0.3 + Math.sqrt(globalMax) * 0.3;

    const dir = new THREE.Vector3().subVectors(end, start).normalize();

    // Calculate the total offset and add extra padding (dependent on the scaleFactor) to push it away from the farthest edge
    const totalOffset = offsetVector.clone().add(offsetVector.clone().normalize().multiplyScalar(scaleFactor));

    // Calculate points with the offset
    const pStart = start.clone().add(totalOffset);
    const pEnd = end.clone().add(totalOffset);

    const distance = pStart.distanceTo(pEnd);

    const coneHeight = scaleFactor;

    // Create the main line (thin cylinder)
    const lineLength = Math.max(0, distance - coneHeight);
    const lineThickness = scaleFactor * 0.04;
    const lineGeo = new THREE.CylinderGeometry(lineThickness, lineThickness, lineLength, 8);
    const lineMat = new THREE.MeshStandardMaterial({ color: hexColor });
    const lineMesh = new THREE.Mesh(lineGeo, lineMat);

    lineMesh.position.copy(pStart).lerp(pEnd, 0.5);
    lineMesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);
    lineMesh.castShadow = true;

    measurementGroup.add(lineMesh);

    // Create a smooth cone geometry
    const coneRadius = scaleFactor * 0.3;
    const coneGeo = new THREE.ConeGeometry(coneRadius, coneHeight, 32);
    const coneMat = new THREE.MeshStandardMaterial({ color: hexColor });

    // First cone (at pStart)
    const arrow1 = new THREE.Mesh(coneGeo, coneMat);
    arrow1.position.copy(pStart);

    // Point the tip toward pStart, set it's castShadow to true and move it inward by half it's length
    arrow1.quaternion.setFromUnitVectors(new THREE.Vector3(0, -1, 0), dir);
    arrow1.position.copy(pStart).add(dir.clone().multiplyScalar(coneHeight / 2));
    arrow1.castShadow = true;

    // Second Cone (at pEnd)
    const arrow2 = new THREE.Mesh(coneGeo, coneMat);
    arrow2.position.copy(pEnd);

    // Point the tip toward pEnd, set it's castShadow to true and move it inward by half it's length
    arrow2.quaternion.setFromUnitVectors(new THREE.Vector3(0, -1, 0), dir.clone().negate());
    arrow2.position.copy(pEnd).sub(dir.clone().multiplyScalar(coneHeight / 2));
    arrow2.castShadow = true;

    measurementGroup.add(arrow1, arrow2);

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    canvas.width = 384;
    canvas.height = 192;

    // Background and round rectangle
    ctx.fillStyle = 'rgba(0,0,0,0.7)';
    ctx.strokeStyle = `#${new THREE.Color(hexColor).getHexString()}`;
    ctx.lineWidth = 8;

    ctx.beginPath();

    if (ctx.roundRect) {
        ctx.roundRect(5, 5, canvas.width - 10, canvas.height - 10, 20);
    } else {
        ctx.rect(5, 5, canvas.width - 10, canvas.height - 10); // Fallback for older browsers
    }

    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = 'white';
    ctx.font = '80px monospace';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    ctx.fillText(labelText, canvas.width / 2, canvas.height / 2);

    const texture = new THREE.CanvasTexture(canvas);
    const spriteMat = new THREE.SpriteMaterial({ map: texture, depthTest: true });
    const label = new THREE.Sprite(spriteMat);

    // Calculate center point
    const centerX = (pStart.x + pEnd.x) / 2;
    const centerY = (pStart.y + pEnd.y) / 2;
    const centerZ = (pStart.z + pEnd.z) / 2;

    const labelPos = new THREE.Vector3(centerX, centerY, centerZ);

    // Find the direction of the line
    const lineDir = new THREE.Vector3().subVectors(pEnd, pStart).normalize();

    // We want to push the label "outward" or "upward"
    // If the line is horizontal (X or Z axis), we push it up or out
    // If the line is vertical (Y axis), we push it to the side
    const up = new THREE.Vector3(0, 1, 0);
    let offsetDir = new THREE.Vector3().crossVectors(lineDir, up).normalize();

    // If the line is perfectly vertical, the cross product above fails (0,0,0)
    // So we check if the line is vertical and use a different axis
    if (offsetDir.length() < 0.1) {
        offsetDir.set(1, 0, 0);
    }

    // Calculate the base center
    const center = new THREE.Vector3().lerpVectors(pStart, pEnd, 0.5);

    // Check if the offsetDir is pointing "inward" toward the model
    // 'center' is the middle of the line. If adding offsetDir makes
    // the point closer to the model's center (0,0,0), we flip it.
    const testPos = center.clone().add(offsetDir);
    if (testPos.length() < center.length()) {
        offsetDir.multiplyScalar(-1);
    }

    // Apply the 0.3 offset in the calculated direction
    labelPos.add(offsetDir.multiplyScalar(scaleFactor));

    // Add a small extra Y bump to move the label strictly above the floor
    labelPos.add(offsetDir.multiplyScalar(scaleFactor));
    labelPos.z += scaleFactor * 0.2;

    label.position.copy(labelPos);

    // Calculate the aspect ratio of the canvas (256 / 128 = 2)
    const aspectRatio = canvas.width / canvas.height;

    // Set the Y scale (height) first, then multiply by aspect ratio for X (width)
    const baseHeight = scaleFactor * 1.75;

    label.scale.set(baseHeight * aspectRatio, baseHeight, 1);

    measurementGroup.add(label);
}

function updateMeasurements(mesh, rawSize) {
    // Remove all existing measurement groups and clean up the memory
    while(measurementGroup.children.length > 0){
        const group = measurementGroup.children[0];

        // Traverse the individual measurement group to find meshes/sprites
        group.traverse((node) => {
            if (node.geometry) node.geometry.dispose();
            if (node.material) {
                if (Array.isArray(node.material)) {
                    node.material.forEach(m => {
                        if (m.map) m.map.dispose();
                        m.dispose();
                    });
                } else {
                    if (node.material.map) node.material.map.dispose();
                    node.material.dispose();
                }
            }
        });

        measurementGroup.remove(group);
    }

    // Get the actual visual box (after scaling)
    const visualBox = new THREE.Box3().setFromObject(mesh);

    const scaledSize = new THREE.Vector3();
    visualBox.getSize(scaledSize);

    const gap = scaledSize.y * 0.2;
    const globalMax = Math.max(scaledSize.x, scaledSize.y, scaledSize.z);

    // Re-create the 3 main dimensions
    // Width (X)
    createMeasurement(
        new THREE.Vector3(visualBox.min.x, visualBox.min.y, visualBox.min.z),
        new THREE.Vector3(visualBox.max.x, visualBox.min.y, visualBox.min.z),
        `${Math.round(rawSize.x)}mm`,
        new THREE.Vector3(0, -gap, 0),
        0xff0000,
        globalMax
    );

    // Length (Y)
    createMeasurement(
        new THREE.Vector3(visualBox.max.x, visualBox.min.y, visualBox.min.z),
        new THREE.Vector3(visualBox.max.x, visualBox.max.y, visualBox.min.z),
        `${Math.round(rawSize.y)}mm`,
        new THREE.Vector3(gap, 0, 0),
        0x00ff00,
        globalMax
    );

    // Height (Z)
    createMeasurement(
    new THREE.Vector3(visualBox.max.x, visualBox.max.y, visualBox.min.z),
    new THREE.Vector3(visualBox.max.x, visualBox.max.y, visualBox.max.z),
        `${Math.round(rawSize.z)}mm`,
        new THREE.Vector3(gap, gap, 0),
        0x0000ff,
        globalMax
    );
}

function fitCameraToObject(mesh, multiplier = 0.7) {
    const boundingBox = new THREE.Box3().setFromObject(mesh);
    const center = boundingBox.getCenter(new THREE.Vector3());
    const size = boundingBox.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);
    const fov = camera.fov * (Math.PI / 180);
    let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2)) * multiplier;

    camera.position.set(
        center.x + cameraZ,
        center.y - cameraZ,
        center.z + cameraZ
    );

    camera.lookAt(center);

    if (controls) {
        controls.target.copy(center);
        controls.update();
    }
}

// Create a new Three.js scene and set it's background color to a dark gray
scene = new THREE.Scene();
scene.background = new THREE.Color(0x202020);

scene.add(measurementGroup);

// Create the camera
camera = new THREE.PerspectiveCamera(45, innerWidth/innerHeight, 0.1, 1000);

camera.up.set(0, 0, 1); // Tell the camera to use the Z axis as the height

// Create a new renderer, set it's size to the innerWidth and innerHeight and append it to the document
renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(innerWidth, innerHeight);
document.body.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// Tell renderer not to clear automatically
renderer.autoClear = false;

// Initialize ViewHelper
const viewHelper = new ViewHelper(camera, renderer.domElement);

document.getElementById('helper-toggle').onchange = (e) => {
    viewHelper.visible = e.target.checked;
};

document.getElementById('dimensions-toggle').onchange = (e) => {
    measurementGroup.visible = e.target.checked;
};

// Add and configure a new ambient light
scene.add(new THREE.AmbientLight(0xffffff, 0.5))

// Configure a directional light and add it to the scene
const dirLight = new THREE.DirectionalLight(0xffffff, 1);
dirLight.position.set(100, -100, 150);

// Enable shadows in the renderer
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

// Update your Directional Light to cast shadows
dirLight.castShadow = true;

// Prevents flickering on the box surface
dirLight.shadow.bias = -0.001;

// The resolution of the shadow texture.
// Higher = sharper shadows but more GPU cost. (Powers of 2: 512, 1024, 2048)
dirLight.shadow.mapSize.width = 1024;
dirLight.shadow.mapSize.height = 1024;

// How close or far an object can be to the light source before it stops casting a shadow.
dirLight.shadow.camera.near = 0.5;
dirLight.shadow.camera.far = 2500;

// Expand the shadow capture area to fit larger boxes
dirLight.shadow.camera.left = -200;
dirLight.shadow.camera.right = 200;
dirLight.shadow.camera.top = 200;
dirLight.shadow.camera.bottom = -200;

scene.add(dirLight);

// size1 = 10 (A major line every 10mm (1cm))
// size2 = 1  (A minor line every 1mm)
const grid = new InfiniteGridHelper(10, 1, new THREE.Color(0xffffff), 1000);
grid.rotation.x = Math.PI / 2; // Rotate the grid by 90 degrees (PI / 2 radians)
grid.position.z = -0.1; // Tiny offset to prevent "Z-fighting" (flickering) with the model floor

scene.add(grid);

document.getElementById("grid-toggle").onchange = (e) => {
    grid.visible = e.target.checked;
}

// Theme (background color)
document.getElementById("theme-select").onchange = (e) => {
    const selectedColor = parseInt(e.target.value);
    const menuButton = document.getElementById("menu-button");
    const uiContainer = document.getElementById('ui-container');

    scene.background = new THREE.Color(selectedColor);

    if (selectedColor > 0x888888) {
        uiContainer.setAttribute("data-theme", "light");

        grid.setColor(0x333333);

        menuButton.style.backgroundColor = "rgba(32, 32, 32, 0.8)";
    } else {
        uiContainer.setAttribute("data-theme", "dark");

        grid.setColor(0xffffff);

        menuButton.style.backgroundColor = "rgba(85, 85, 85, 0.8)";
    }
};

fetch("./model.stl")
    .then(response => {
        if (response.ok) {
            loader.load("./model.stl", geometry => {
                // Load and compute the model.stl file
                geometry.center();
                geometry.computeBoundingBox();

                const size = new THREE.Vector3();
                geometry.boundingBox.getSize(size);

                // Create mesh
                const mesh = new THREE.Mesh(geometry, new THREE.MeshStandardMaterial({ color: 0xff0000 }))
                currentMesh = mesh;

                // Shift the geometry up so the bottom is the pivot
                geometry.translate(-size.x / 2, size.y / 2, size.z / 2);
                mesh.position.set(0, 0, 0);

                scene.add(mesh);

                fitCameraToObject(currentMesh, 0.7);

                updateMeasurements(currentMesh, size);

                controls.update();

                controls.saveState();

                // Signal Python to unlock the button
                if (window.pybridge && typeof window.pybridge.on_viewer_ready === "function") window.pybridge.on_viewer_ready();
            }, undefined, e => console.error(e))
        } else {
            console.log("[WARNING] No initial model found; starting with empty grid.");

            // Signal Python to unlock the button
            // if (window.pybridge && typeof window.pybridge.on_viewer_ready === "function") window.pybridge.on_viewer_ready();
        }
    })
    .catch(err => {
        console.log("[WARNING] Ignoring initial 404 - Grid should still show.");
    });

// Handle the resizing of the window
window.addEventListener("resize", () => {
    camera.aspect = innerWidth / innerHeight;

    camera.updateProjectionMatrix();

    renderer.setSize(innerWidth, innerHeight);
});

window.updateMesh = function(url) {
    loader.load(url, function (geometry) {
        // Remove old mesh
        if (currentMesh) {
            scene.remove(currentMesh);

            // Remove from memory
            currentMesh.geometry.dispose();
            currentMesh.material.dispose();
        }

        // Setup new geometry
        geometry.center();
        geometry.computeBoundingBox();

        const size = new THREE.Vector3();
        geometry.boundingBox.getSize(size);

        currentMesh = new THREE.Mesh(geometry, new THREE.MeshStandardMaterial({ color: 0xff0000 }));

        geometry.translate(-size.x / 2, size.y / 2, size.z / 2);
        currentMesh.position.set(0, 0, 0);

        scene.add(currentMesh);

        if (autoFitEnabled) {
            fitCameraToObject(currentMesh, 0.7);
        }

        // Re-create the measurements with the new size
        updateMeasurements(currentMesh, size);
    }, undefined, function(err) {
        console.error("[viewer.html] Error: ", err);
    });
};

window.setLoading = function() {
    const text = document.getElementById("loader-text");
    const loader = document.getElementById("loader-spinner");

    loader.style.display = "block"; // Hide spinner initially

    text.innerHTML = "<h2>Initializing Engine...</h2><i>Please wait...</i>";

    return true;
};

window.revealViewer = function() {
    const loader = document.getElementById("loader-container");
    const menuButton = document.getElementById("menu-button");

    if (loader) loader.classList.add("fade-out");
    if (menuButton) menuButton.style.opacity = "1";
};

// Render the scene
(function animate() {
    requestAnimationFrame(animate);

    controls.update();

    renderer.clear();

    // Render main scene (full window)
    renderer.render(scene, camera);
    labelRenderer.render(scene, camera);
    viewHelper.render(renderer);
})();
