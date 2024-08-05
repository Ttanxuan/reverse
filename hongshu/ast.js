function get_decrypt(){
    const traverse = require("@babel/traverse").default;
    const {parse} = require("@babel/parser");
    const generator = require("@babel/generator").default;
    const fs = require("fs");
    const types = require("@babel/types");

    var js_code = fs.readFileSync('hongshuconfound.js', {encoding: 'utf-8'});  //通过fs读取文件，防止电脑出现未知错误
    const ast_code = parse(js_code)

    // 获取解密函数并写入内存
    let member_decode_js = '';

    for(i=6;i<9;i++){
        member_decode_js += generator(ast_code.program.body[i]).code;
    }
    eval(member_decode_js)
    // console.log(_0xcbc4('0x0'))


// 需要加入的代码
    let my_code0 = 'document = {\n' +
        '  \'type\': \'text/css\'\n' +
        '};\n' +
        'top = {\n' +
        '  \'window\':{\n' +
        '    \'location\':{\n' +
        '      \'href\':\'href0\'\n' +
        '\n' +
        '    }\n' +
        '  }\n' +
        '}\n' +
        'window={\n' +
        '    \'location\':{\n' +
        '      \'href\':\'href1\'\n' +
        '\n' +
        '    }\n' +
        '  }'
    let my_code1 = 'function get_word(i){\n' +
        '  return words[i]\n' +
        '}'

// 去掉document的部分
    var data_code = ''
    for (i = 0; i < 25; i++) {
        if ((i >= 18 && i <= 22) || i == 24) {
            continue
        } else {
            data_code += generator(ast_code.program.body[i]).code;
        }

    }


    // //visitor对修改的内容进行定义 定义规则
    // let name = ast_code.program.body[8].declarations[0].id.name
    // console.log(name)
    // const visitor ={
    //     CallExpression(path){
    //         if(path.node.callee.name === name && path.node.arguments[0].type === 'StringLiteral'){
    //             path.replaceInline(types.valueToNode(eval(path.toString())))
    //             // console.log(path)
    //             // throw ''
    //         }
    //     },
    //
    //     // StringLiteral(path){
    //     //     // console.log(path.node.extra)
    //     //     // throw  ''
    //     //     if(path.node.extra){
    //     //         // path.node.extra.raw = '\'' + path.node.value + '\''
    //     //         delete path.node.extra
    //     //     }
    //     // }
    //     // BinaryExpression(path){
    //     //     if(path.node.left.type === 'StringLiteral' && path.node.right.type === 'StringLiteral' && path.node.operator === '+'){
    //     //         path.replaceInline(types.valueToNode(path.node.left + path.node.right)) //types.valueToNode() 用于将 JavaScript 值转换为 AST 节点，以便将其插入到 AST 中。
    //     //     }
    //     // },
    //     // MemberExpression:{
    //     //     exit(path){
    //     //         if(path.node.computed && path.node.property.type === 'StringLiteral'){
    //     //         path.node.computed = false;
    //     //         path.node.property.type = "Identifier";
    //     //         path.node.property.name = path.node.property.value;
    //     //         delete path.node.property.value;
    //     //         // console.log(path.node.property.name)
    //     //         // throw  ''
    //     //     }
    //     //     }
    //     // }
    // };
    //
    // traverse(ast_code,visitor);
    // const result_js_code = generator(ast_code).code;
    // // console.log(result_js_code)


// 重组js代码
    var data_code = my_code0 + '\n' + data_code + '\n' + my_code1
// 写入文件
    fs.writeFile('./after_confound.js', data_code, {flag: 'w'}, (err) => {
        if (err) {
            console.error('写入文件时发生错误：', err);
        }
    });
}
get_decrypt()


