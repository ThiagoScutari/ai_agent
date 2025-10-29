# 1_Fundamentos

*   **Pergunta:** Qual a definição e o propósito principal do programa "Hello, World!" na introdução à programação?

    O programa "Hello, World!" é um programa de computador simples que exibe uma mensagem de saudacção, como "Hello, world!". Seu propósito principal é servir como um teste fundamental para confirmar que uma linguagem de programação está instalada e configurada corretamente, e que o compilador ou interpretador está funcionando como esperado. É comumente o primeiro programa que os iniciantes escrevem ao aprender uma nova linguagem de programação, oferecendo uma experiência inicial bem-sucedida de codificação e execução, validando assim o ambiente de aprendizado e proporcionando uma sensação de realização. A prática se origina de um exemplo de 1978 na linguagem de programação C. [Fonte: pt.wikipedia.org]

*   **Pergunta:** Quais são os elementos de código mais comuns para implementar um "Hello, World!" em linguagens populares (ex: Python, JavaScript, Java)?

    A implementação de um programa "Hello, World!" envolve o uso de funções ou métodos específicos de cada linguagem para a saída de dados.

    *   **Python:** A implementação mais direta utiliza a função `print()`. O texto a ser exibido, como "Hello, World!", é colocado entre parênteses e entre aspas duplas ou simples. Exemplo: `print("Hello, World!")`. [Fonte: programiz.com]

    *   **JavaScript:** Diversos métodos podem ser usados para exibir a saída. Para um "Hello, World!" básico, frequentemente destinado à depuração ou saída no console, `console.log("Hello, World!")` é comum. Outros métodos incluem `document.write("Hello, World!")` (embora possa sobrescrever o conteúdo existente), `alert("Hello, World!")` para uma caixa de alerta pop-up, ou a manipulação de elementos HTML usando `document.getElementById("someElementId").innerHTML = "Hello, World!";`. [Fonte: w3schools.com]

    *   **Java:** Um programa "Hello, World!" em Java requer a definição de uma classe e um método `main`, que serve como ponto de entrada. A saída é tipicamente gerenciada por `System.out.println("Hello, World!");`. A estrutura do código envolve:
        ```java
        public class HelloWorld {
            public static void main(String[] args) {
                System.out.println("Hello, World!");
            }
        }
        ```
        [Fonte: geeksforgeeks.org]