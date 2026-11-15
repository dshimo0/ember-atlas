import test from 'node:test';
import assert from 'node:assert/strict';
import {signed,number} from '../web/format.mjs';
test('unavailable residuals are not presented as signed zero',()=>{
 for(const value of [null,undefined,NaN])assert.equal(signed(value),'—');
 assert.equal(signed(0),'0.0');assert.equal(number(null),'—');assert.equal(signed(-2),'−2.0');
});
