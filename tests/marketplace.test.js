import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
const app=readFileSync(new URL('../app.js',import.meta.url),'utf8');
const districtsExpression=app.match(/const districts=(\{.*?\});\nconst supportedCountries=/s)?.[1];
test('Rwanda district selector contains 30 unique official districts',()=>{
 assert.ok(districtsExpression,'district data defined');
 const districts=JSON.parse(districtsExpression);
 assert.equal(Object.keys(districts).length,30);
 for(const name of ['Gasabo','Kicukiro','Nyarugenge','Gisagara','Ruhango','Burera','Gicumbi','Gatsibo','Kirehe','Nyamasheke','Rusizi'])assert.ok(districts[name],name);
});
test('marketplace supports real buyer requests and private inquiries',()=>{
 assert.match(app,/listing_type:data\.type/);
 assert.match(app,/data-market-contact/);
 assert.match(app,/market_inquiries/);
 assert.match(app,/await state\.supabase\.from\('market_listings'\)\.insert\(payload\)/);
 assert.doesNotMatch(app,/Buyer offers are not yet supported/);
});
test('international marketplace does not falsely generalize Rwanda NASA history',()=>{
 assert.match(app,/state\.country!=='Rwanda'/);
 assert.match(app,/supportedCountries=/);
 assert.match(app,/state\.marketCloud\|\|\[\]/);
});
