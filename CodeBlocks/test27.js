/*
 
 Author: valetolpegin@gmail.com ( Vale Tolpegin )
 *Copyright 2014 Vale Tolpegin.
 *
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 
 */
'use strict';

if ( !Blockly.Language )
    Blockly.Language = {};

Blockly.spin = Blockly.Generator.get( 'spin' );

Blockly.Language.HelloWorld = {
	category: 'LameStation',
	helpUrl: '',
	init: function() {
		this.appendValueInput( 'hi' )
			.appendTitle( "get hi" );
		this.appendValueInput( 'ie' )
			.appendTitle( "get ie" );
		this.setPreviousStatement( true, null );
		this.setNextStatement( true, null );
	}
}

Blockly.spin.HelloWorld = function() {
	Blockly.spin.setups_[ "LameStation_hi" ] = "int hi";
	Blockly.spin.setups_[ "LameStation_ie" ] = "int ie";

	var hi = Blockly.Spin.valueToCode( this, 'hi' );
	var ie = Blockly.Spin.valueToCode( this, 'ie' );

	var code = "	" + ie + " <= " + hi + "";
	return code;
};

Blockly.Language.Test = {
	category: 'LameStation',
	helpUrl: '',
	init: function() {
		this.appendValueInput( 'hi' )
			.appendTitle( "get hi" );
		this.appendValueInput( 'ie' )
			.appendTitle( "get ie" );
		this.setPreviousStatement( true, null );
		this.setNextStatement( true, null );
	}
}

Blockly.spin.Test = function() {
	Blockly.spin.setups_[ "LameStation_hi" ] = "int hi";
	Blockly.spin.setups_[ "LameStation_ie" ] = "int ie";

	var hi = Blockly.Spin.valueToCode( this, 'hi' );
	var ie = Blockly.Spin.valueToCode( this, 'ie' );

	var code = "	" + ie + " >! " + hi + "";
	return code;
};

