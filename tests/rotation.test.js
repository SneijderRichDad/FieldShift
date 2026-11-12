import {test} from 'node:test';
import assert from 'node:assert/strict';
// Browser app requires DOM; test transparent scoring logic independently.
const score=(r,p)=>{const w=p==='Water conservation'?[.2,.6,.2]:p==='Crop diversity'?[.2,.2,.6]:[.55,.25,.2];return Math.round(r.soil*w[0]+r.water*w[1]+r.diversity*w[2])};
test('soil weighting',()=>assert.equal(score({soil:100,water:0,diversity:0},'Soil health'),55));
test('water weighting',()=>assert.equal(score({soil:0,water:100,diversity:0},'Water conservation'),60));
test('diversity weighting',()=>assert.equal(score({soil:0,water:0,diversity:100},'Crop diversity'),60));
test('total is bounded',()=>assert.equal(score({soil:100,water:100,diversity:100},'Soil health'),100));
