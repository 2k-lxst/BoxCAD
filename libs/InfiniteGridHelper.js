// Author: Fyrestar https://mevedia.com (https://github.com/Fyrestar/THREE.InfiniteGridHelper)
// Modified by: 2klxst

import * as THREE from 'three';

export class InfiniteGridHelper extends THREE.Mesh {
    constructor(size1 = 10, size2 = 1, color = new THREE.Color('white'), distance = 8000) {
        const geometry = new THREE.PlaneGeometry(2, 2, 1, 1);
        const material = new THREE.ShaderMaterial({
            side: THREE.DoubleSide,
            uniforms: {
                uSize1: { value: size1 },
                uSize2: { value: size2 },
                uColor: { value: color },
                uDistance: { value: distance }
            },
            transparent: true,
            vertexShader: `
                varying vec3 worldPosition;
                uniform float uDistance;
                void main() {
                    vec3 pos = position.xzy * uDistance;
                    pos.xz += cameraPosition.xz;
                    worldPosition = pos;
                    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
                }
            `,
            fragmentShader: `
                varying vec3 worldPosition;
                uniform float uSize1;
                uniform float uSize2;
                uniform vec3 uColor;
                uniform float uDistance;

                float getGrid(float size) {
                    vec2 r = worldPosition.xz / size;
                    vec2 grid = abs(fract(r - 0.5) - 0.5) / fwidth(r);
                    float line = min(grid.x, grid.y);
                    return 1.0 - min(line, 1.0);
                }

                void main() {
                    float d = 1.0 - min(distance(cameraPosition.xz, worldPosition.xz) / uDistance, 1.0);
                    float g1 = getGrid(uSize1);
                    float g2 = getGrid(uSize2);
                    float strength = mix(g2 * 0.2, g1, g1);
                    gl_FragColor = vec4(uColor.rgb, strength * pow(d, 3.0));
                    if (gl_FragColor.a <= 0.0) discard;
                }
            `,
            extensions: { derivatives: true }
        });

        super(geometry, material);
        this.frustumCulled = false;
    }

    setColor(color) {
        const newColor = (color instanceof THREE.Color) ? color: new THREE.Color(color);

        this.material.uniforms.uColor.value.copy(newColor);
    }
}
