-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 18-Maio-2024 às 15:26
-- Versão do servidor: 10.4.28-MariaDB
-- versão do PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `db_g14`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `administrador`
--

CREATE TABLE `administrador` (
  `utilizador_ptr_id` int(11) NOT NULL,
  `gabinete` varchar(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `administrador`
--

INSERT INTO `administrador` (`utilizador_ptr_id`, `gabinete`) VALUES
(1, ''),
(23, 'Edifício 2, Gabinete 1.5.2');

-- --------------------------------------------------------

--
-- Estrutura da tabela `anfiteatro`
--

CREATE TABLE `anfiteatro` (
  `EspacoID` int(11) NOT NULL,
  `EspacoEdificio` varchar(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `arlivre`
--

CREATE TABLE `arlivre` (
  `EspacoID` int(11) NOT NULL,
  `EspacoEdificio` varchar(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `atividade`
--

CREATE TABLE `atividade` (
  `ID` int(11) NOT NULL,
  `Nome` varchar(255) NOT NULL,
  `Descricao` longtext NOT NULL,
  `Publicoalvo` varchar(255) NOT NULL,
  `nrColaboradoresNecessario` int(11) NOT NULL,
  `Tipo` varchar(64) NOT NULL,
  `Estado` varchar(64) NOT NULL,
  `dataSubmissao` datetime(6) NOT NULL,
  `dataAlteracao` datetime(6) NOT NULL,
  `duracaoEsperada` int(11) NOT NULL,
  `participantesMaximo` int(11) NOT NULL,
  `diaAbertoID` int(11) NOT NULL,
  `EspacoID` int(11) NOT NULL,
  `ProfessorUniversitarioUtilizadorID` int(11) NOT NULL,
  `Tema` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `atividade`
--

INSERT INTO `atividade` (`ID`, `Nome`, `Descricao`, `Publicoalvo`, `nrColaboradoresNecessario`, `Tipo`, `Estado`, `dataSubmissao`, `dataAlteracao`, `duracaoEsperada`, `participantesMaximo`, `diaAbertoID`, `EspacoID`, `ProfessorUniversitarioUtilizadorID`, `Tema`) VALUES
(7, 'Recursos Naturais e Biotecnologia', 'A atividade geral RECURSOS NATURAIS E BIOTECNOLOGIA inclui três atividades específicas integradas na área da biotecnologia: (a) As plantas, a luz e a fotossíntese; (b) Como cultivar plantas em tubos de ensaio; e (c) A bioengenharia na produção de biocombustíveis. Estas três atividades apresentam uma duração de 45 minutos cada e serão frequentadas, sequencialmente, por três grupos de alunos visitantes. \r\n\r\nPúblico-alvo: 9º - 12º ano, área ciências e tecnologia. Tipologia da atividade geral: laboratorial.\r\n\r\n(a) As plantas, a luz e a fotossíntese\r\nEsta atividade inclui a observação da fotossíntese em ervas marinhas e a extração, separação, observação e identificação de pigmentos fotossintéticos de vários tipos de folhas.\r\nResponsável: Isabel Barrote.\r\nLocal: Edifício 8, laboratório 2.30.\r\n\r\n(b) Como cultivar plantas em tubos de ensaio\r\nNesta atividade os alunos terão oportunidade de contatar com a técnica de cultura in vitro de tecidos vegetais que permite a produção de plantas em ambiente laboratorial controlado.\r\nResponsáveis: Anabela Romano e Sandra Gonçalves.\r\nLocal: Edifício 8, laboratório 3.43.\r\n\r\n(c) A bioengenharia na produção de biocombustíveis\r\nEsta atividade inclui a visita ao Laboratório de Engenharia e Biotecnologia Ambiental, onde os alunos poderão conhecer os trabalhos em curso que utilizam diferentes tipos de microrganismos para produzir biocombustíveis alternativos, amigos do ambiente. Os alunos terão oportunidade de acompanhar e desenvolver uma atividade com um sistema biológico para a produção de bioetanol. Terão ainda contato com sistemas de microalgas, utilizados para a produção de diferentes produtos de interesse comercial. \r\nResponsável: Sara Raposo.\r\nLocal: Edifício 8, laboratório 2.43.', 'Ciencias e Tecnologia', 5, 'Atividade Laboratorial', 'Aceite', '2022-02-23 16:11:25.699722', '2022-03-03 12:19:50.159759', 180, 45, 3, 29, 25, 4),
(8, 'Desafios nos Laboratórios de Química e Ciências Farmacêuticas', 'As atividades especifícas a que terás oportunidade de assistir vão desde:\r\n- A extração de compostos naturais com atividade biológica, à sua formulação, (Vamos fazer pomadas, comprimidos, etc), e saber um pouco sobre a atuação do medicamento no corpo humano, Vamos perceber a relação fármaco-recetor. \r\nJá no controlo de qualidade dos medicamentos, Vamos identificar fármacos presentes num comprimido.  \r\n- E quando há um problema de saúde a Farmácia Comunitária e o Farmacêutico surgem de imediato na nossa mente - PharmaHelp – Do problema à solução!\r\n- Quando é que acaba a pandemia? Uma experiência de cinética é uma das atividades propostas, em que a reação química serve como pano de fundo, que liga com a disciplina da cinética química, contudo a interatividade será com o modelo SIR em Matlab, propondo diferentes parâmetros de doenças, populações, R0, taxas de vacinação, etc.\r\nPodemos ainda observar o fenómeno de oscilação numa reação química -  Semáforo Químico - A Reação de Belousov-Zhabotinskii, através da realização por alunos desta experiência química simples, integrada na área de estudo de Química-Física / Cinética Química. \r\n\r\nIdentificação do público alvo: 10º, 11º, 12º Ano\r\n\r\nLocal onde decorrem as atividades: Departamento de Química e Farmácia da Faculdade de Ciências e Tecnologia, Campus de Gambelas; Edificio 2: Lab de simulação farmacêutica; Lab 1.19; Lab 2.23\r\n\r\nResponsável: Ana Grenha; Ana Serralheiro; Carolina Rio; Custódia Fonseca; Graça Miguel; Isabel Ramalhinho; Jaime Conceição; Mónica Condinho; Wenli Wang e Rui Borges e alunos do NeciFarm.', 'Ciencias e Tecnologia', 3, 'Atividade Laboratorial', 'Aceite', '2022-02-23 19:10:09.309075', '2022-03-03 12:02:27.096099', 180, 45, 3, 30, 26, 4),
(10, 'Tecnologia na nossa vida', 'A atividade geral TECNOLOGIA NA NOSSA VIDA inclui três atividades específicas integradas na área da informática: (a) O jogo LINA; (b) Centro de dados e Rede Informática; (c) Projetos durante e pós curso, apresentação do NEEI. Estas três atividades específicas apresentam uma duração de 50 minutos cada e serão frequentadas, sequencialmente, por três grupos de alunos visitantes. \r\n\r\nPúblico-alvo: 9º e 10º - 12º ano\r\n\r\n(a)	O jogo LINA \r\nLINA é um jogo sério para telemóvel que utiliza realidade aumentada, teatro interactivo, narrativa, e colaboração entre jogadores para promover o sentimento de pertença e coesão social numa turma, para além de alertar para os problemas de saúde mental.  Foi desenvolvido no contexto de um projeto de investigação internacional e multidisciplinar (https://dot.lbg.ac.at/), e demonstra o que se consegue fazer quando se juntam colaboradores de engenharia informática, psicologia, artes, e teatro. \r\n\"Num dia normal de escola, o professor faz a chamada ... mas há um nome em falta. Onde está a Lina? E o que está no caderno misterioso que ela deixou debaixo da minha mesa?\"\r\nUsando uma história de mistério, e narrativa interactiva, os jogadores utilizam realidade aumentada no telemóvel para procurar e descobrir artefactos deixados na sala de aula por uma colega ficcional. O jogo conduz os jogadores para uma interação cara-a-cara, em que devem colaborar para resolver os puzzles e desbloquear a história sobre o que aconteceu à Lina.\r\n\r\nResponsável: João Dias\r\nLocal: Edifício 1-Sala 1.53\r\n\r\n(b) Centro de dados e Rede Informática \r\n•	Centro de Dados da Universidade do Algarve – apresentação das tecnologias, infraestrutura e conetividade do Centro de Dados da UAlg \r\n•	A minha primeira rede informática – Criação da uma rede informática em Laboratório de Redes para, através de simulador, criar a primeira rede informática utilizando configuração de Vlans e roteamento externo entre dois locais remotos\r\nResponsáveis: Joel Guerreiro e Luís Pisco.\r\nLocal: Edifício 1-Salas 1.41 (centro de dados) e 0.17 (rede informática)\r\n\r\n\r\n\r\n(c)	Projetos durante e pós curso. Apresentação do NEEI\r\n•	Demonstração de diversos projetos desenvolvidos ao longo do curso, visando abranger\r\no maior número de unidades curriculares. O propósito desta atividade específica é mostrar aos alunos os projetos que eles mesmos poderão desenvolver caso ingressem na\r\nUniversidade do Algarve. Para além disso, serão ainda apresentados projetos\r\ndesenvolvidos pelos alunos fora das unidades curriculares, nos quais o conhecimento adquirido no curso, foi imprescindível para a sua elaboração.\r\n•	Conversa com os alunos visitantes com o intuito de mostrar em que consiste o núcleo de\r\nestudantes, apresentar a sua missão e quais os seus objetivos.\r\n\r\nResponsável: Núcleo de estudantes de Engenharia informática\r\nLocal: Edifício 1-Sala 1.63', 'Ciencias e Tecnologia', 3, 'Misto', 'Aceite', '2022-03-01 22:59:47.182199', '2023-04-19 09:34:31.772402', 150, 45, 3, 33, 26, 4),
(11, 'Matemática para sempre', 'A atividade geral MATEMÁTICA NA VIDA inclui três atividades específicas integradas na área da matemática: (a) A navegação e o desenvolvimento tecnológico; (b) Será que tens o que é preciso para ser o próximo milionário?; (c) Algarismos de controlo. Estas três atividades específicas apresentam uma duração de 45 minutos cada e serão frequentadas, sequencialmente, por três grupos de alunos visitantes.\r\n\r\nPúblico-alvo: 10º - 12º ano\r\n\r\n(a) A navegação e o desenvolvimento tecnológico \r\nDesde os primórdios da Humanidade os homens precisaram de descobrir a forma de se orientarem na deslocação entre dois pontos da esfera terrestre. As respostas às perguntas “Onde estamos?” e “Qual é a direção correta?” foram dadas por alguns dos mais brilhantes cientistas da história e estiveram na base de importantes avanços tecnológicos. \r\nNo contexto atual, voltamos a levantar as mesmas questões e a nossa história conjunta mostra que as respostas passam pelo desenvolvimento tecnológico, a ciência e o ensino de qualidade.\r\n\r\nResponsável: Juan Rodríguez\r\nLocal: Edifício 2-Sala de seminários\r\n\r\n(b) Será que tens o que é preciso para ser o próximo milionário?\r\nVem descobrir o curso de Matemática Aplicada à Economia e à Gestão e como estes 3 mundos podem mudar a tua vida. Vamos fazer um pequeno jogo, mostrar o que difere este curso dos restantes e responder às tuas questões. Será que tens o que é preciso para ser o próximo Ellon Musk?\r\n\r\nResponsável: NEMAEG-Núcleo de Estudantes de Matemática Aplicada à Economia e à Gestão\r\nLocal: Edifício 2-Sala 3.????\r\n\r\n(c) Algarismos de controlo\r\nOs algarismos de controlo servem para detetar se há erros nas sequências de números que compõem os vários sistemas de identificação que utilizamos no dia-a-dia: bilhete de identidade, número de contribuinte, número do passaporte, códigos de barras, NIB, notas de euro, códigos ISBN para livros, etc. Os erros mais frequentes quando lidamos com sequências grandes de algarismos é a troca de algarismos consecutivos (ex: 49 em vez de 94) ou o erro num dos algarismos (ex: 3 em vez de 8). Vamos aprender a calcular o algarismo de controlo nos códigos de barras e analisar as (des)vantagens deste método. Tragam objetos com código de barras para a atividade para confirmarmos que estes estão corretos.\r\n\r\nSe possível, os alunos devem trazer material de escrita, calculadora e um objeto com código de barras.\r\n\r\nResponsável: Diana Rodelo\r\nLocal: Edifício 2-Sala 3.????', 'Ciencias e Tecnologia', 3, 'Misto', 'Aceite', '2022-03-01 23:08:32.088596', '2022-03-10 18:56:02.216542', 180, 45, 3, 30, 26, 4),
(12, 'Física e Matemática, ontem e hoje', 'A atividade geral FÍSICA E MATEMÁTICA, ONTEM E HOJE inclui três atividades específicas integradas na área da física e matemática: (a) Carga Específica do Eletrão (Experiência de Thomson); (b) A navegação e o desenvolvimento tecnológico; (c) Algarismos de controlo. Estas três atividades específicas apresentam uma duração de 45 minutos cada e serão frequentadas, sequencialmente, por três grupos de alunos visitantes. \r\n\r\nPúblico-alvo: 10º - 12º ano\r\n\r\n(a)	Carga Específica do Eletrão (Experiência de Thomson)\r\nAtravés de um feixe de eletrões, obtido com um tubo de raios catódicos, Thomson determinou a carga do eletrão dividida pela sua massa.\r\n\r\nResponsável: José Luís Argain\r\nLocal: Edifício 2-Lab 3.28\r\n\r\n(b)	A navegação e o desenvolvimento tecnológico \r\nDesde os primórdios da Humanidade os homens precisaram de descobrir a forma de se orientarem na deslocação entre dois pontos da esfera terrestre. As respostas às perguntas “Onde estamos?” e “Qual é a direção correta?” foram dadas por alguns dos mais brilhantes cientistas da história e estiveram na base de importantes avanços tecnológicos. \r\nNo contexto atual, voltamos a levantar as mesmas questões e a nossa história conjunta mostra que as respostas passam pelo desenvolvimento tecnológico, a ciência e o ensino de qualidade.\r\n\r\nResponsável: Juan Rodríguez\r\nLocal: Edifício 2-Sala de seminários\r\n\r\n(c) Algarismos de controlo\r\nOs algarismos de controlo servem para detetar se há erros nas sequências de números que compõem os vários sistemas de identificação que utilizamos no dia-a-dia: bilhete de identidade, número de contribuinte, número do passaporte, códigos de barras, NIB, notas de euro, códigos ISBN para livros, etc. Os erros mais frequentes quando lidamos com sequências grandes de algarismos é a troca de algarismos consecutivos (ex: 49 em vez de 94) ou o erro num dos algarismos (ex: 3 em vez de 8). Vamos aprender a calcular o algarismo de controlo nos códigos de barras e analisar as (des)vantagens deste método. Tragam objetos com código de barras para a atividade para confirmarmos que estes estão corretos.\r\n\r\nSe possível, os alunos devem trazer material de escrita, calculadora e um objeto com código de barras.\r\n\r\nResponsável: Diana Rodelo\r\nLocal: Edifício 2-Sala 3.????', 'Ciencias e Tecnologia', 1, 'Misto', 'Aceite', '2022-03-01 23:11:52.860442', '2023-04-19 09:21:19.078054', 60, 45, 3, 30, 26, 4),
(13, 'SOS URBAN: espaços verdes sustentáveis', 'A atividade geral SOS URBAN: ESPAÇOS VERDES SUSTENTÁVEIS inclui duas atividades específicas integradas na área da arquitetura paisagista: (a) SOS URBAN: arquitetura paisagista e alterações climáticas; e (b) Do projeto ao jardim. Estas duas atividades apresentam uma duração de 60 minutos cada e serão frequentadas, sequencialmente, por dois grupos de alunos visitantes. \r\n\r\nPúblico-alvo: 9º - 12º ano, área ciências e tecnologia. Tipologia da atividade geral: mista.\r\n\r\n(a) SOS URBAN: Arquitetura Paisagista e Alterações Climáticas\r\nA arquitetura paisagista é uma profissão especialmente preparada para enfrentar os grandes desafios das alterações climáticas, quer no âmbito do ordenamento do território e da conservação da natureza, quer à escala das cidades, onde se impõem mudanças para uma maior sustentabilidade urbana. Nesta atividade revelamos a profissão e mostramos exemplos de projetos que lidam diretamente com estes desafios. Depois de uma breve apresentação do tema da sustentabilidade urbana, segue-se uma atividade prática onde os alunos, trabalhando em equipas, assumem o papel de decisores na adoção de práticas de sustentabilidade, para a melhoria de uma zona urbana. No final cada equipa disporá de seis minutos para apresentar as suas soluções e propostas. Os alunos poderão também descobrir qual o percurso de um estudante universitário de arquitetura paisagista na Universidade do Algarve, o seu dia-a-dia, a diversidade das matérias aprendidas e o seu trabalho prático. \r\nResponsáveis: Paula Gomes da Silva e Desidério Baptista.\r\nLocal: Edifício 8, sala 3.44.\r\n\r\n(b) Do projeto ao jardim\r\nEsta atividade prática pretende motivar os alunos para a conceção e execução de projetos de jardins e de espaços exteriores e inclui a montagem de um projeto de rega e a execução de um plano de plantação. Os alunos recebem um miniprojecto de um jardim (rega e plano de plantação) para o local e sua interpretação. Com este projeto irão piquetar os principais elementos do jardim, montar o sistema de rega à superfície e colocar as plantas envasadas no seu local de plantação.\r\nResponsável: José António Monteiro.\r\nLocal: espaço exterior, Campus de Gambelas.', 'Ciencias e Tecnologia', 2, 'Misto', 'Aceite', '2022-03-03 11:15:04.894347', '2022-03-03 12:18:57.127518', 150, 30, 3, 29, 25, 4),
(14, 'O cultivo das plantas: the sky is the limit!', 'A atividade  geral CULTIVO DE PLANTAS: THE SKY IS THE LIMIT! inclui três atividades específicas integradas na área das ciências agrárias: (a) Avaliar e preservar a qualidade de frutos e legumes; (b) Voa na boa … sobre as plantas!; e (c) Operação de sistemas de cultivo sem solo de plantas hortícolas. Estas três atividades apresentam uma duração de 45 minutos cada e serão frequentadas, sequencialmente, por três grupos de alunos visitantes. \r\n\r\nPúblico-alvo: 10º - 12º ano, área ciências e tecnologia. Tipologia da atividade geral: mista.\r\n\r\n(a) Avaliar e preservar a qualidade de frutos e legumes\r\nEsta atividade pretende sensibilizar os alunos para a importância qualitativa e nutricional dos frutos e legumes frescos e a melhor forma de os conservar. Os produtos hortofrutícolas continuam os seus processos metabólicos a um ritmo elevado após a sua colheita, o que os torna altamente perecíveis. É também cada vez maior a exigência do consumidor em relação à qualidade dos produtos. É deste modo imprescindível que existam técnicos especializados na área da pós-colheita de produtos hortofrutícolas. Estes técnicos devem conhecer e implementar técnicas que abrandem os processos de deterioração pós-colheita e que permitem manter o valor de mercado e a segurança alimentar dos produtos hortofrutícolas. A atividade prática inclui \r\numa visita à estação e ao laboratório da pós-colheita e sala de provas organoléticas e a determinação de parâmetros de avaliação de qualidade em frutos e legumes e provas organoléticas a realizar no laboratório.\r\nResponsáveis: Custódia Gago, Adriana Guerreiro e Maria Dulce Antunes.\r\nLocal: Edifício 8, laboratório 1.31 e sala de provas. \r\n\r\n(b) Voa na boa … sobre as plantas!\r\nEsta atividade prática inclui uma breve apresentação teórica dos conceitos de agricultura de precisão e como pode o Homem e a tecnologia monitorizar e decidir que práticas culturais deve adotar. Aborda, de forma específica, os sistemas de navegação por satélite, com referência à utilização de drones e câmaras multiespectrais para avaliar o estado das culturas. Inclui uma demonstração prática da utilização de drones com câmara multiespectral, tratamento da informação para avaliar o estado da vegetação e o cálculo de um mapa do índice de vegetação por diferença normalizada (NDVI). \r\nResponsáveis: Carlos Guerrero e Pedro Luiz.\r\nLocal: Horto (Campus de Gambelas) e espaço exterior.\r\n\r\n(c) Operação de sistemas de cultivo sem solo de plantas hortícolas\r\nOs sistemas de cultivo de plantas hortícolas sem recurso ao solo - em sistemas hidropónicos ou em substratos - conhecidos popularmente por “hidroponia”, requerem o controlo constante e rigoroso das condições de desenvolvimento das plantas, mas permitem aumentar a produção por unidade de área, bem como a eficiência de uso de factores de produção como a água ou os fertilizantes, de entre outras importantes vantagens. Nesta atividade, os alunos ficarão a conhecer quais os fatores ambientais cujo controlo é mais importante e de que forma se efectua o seu controlo e visitarão culturas em curso nestes sistemas de cultivo. \r\nResponsável: Mário Reis.\r\nLocal: Horto (Campus de Gambelas).', 'Ciencias e Tecnologia', 3, 'Misto', 'Aceite', '2022-03-03 11:21:15.784539', '2022-03-03 12:18:49.915707', 180, 45, 3, 32, 25, 4),
(15, 'As 20 000 léguas subterrâneas', 'A atividade geral AS 20 000 LÉGUAS SUBTERRÂNEAS inclui duas atividades específicas integradas na gestão de recursos hídricos, em particular os subterrâneos dada a sua importância, uma vez que constituem a principal, ou única, origem de água doce em muitas regiões do planeta. A atividade demonstra a componente subterrânea do ciclo da água e a sua relação com as águas superficiais: (a) Modelo físico e funcionamento de um aquífero; e (b) Monitorização de águas subterrâneas e intrusão salina. Estas duas atividades apresentam uma duração de 60 minutos cada e serão frequentadas, sequencialmente, por dois grupos de alunos visitantes.  Entre as duas atividades, os alunos percorrem o eco-circuito do Campus de Gambelas, onde se apresentam placas botânicas contendo um índice de vulnerabilidade às alterações climáticas. Este percurso serve de ligação entre as componentes superficial e a subterrânea do ciclo da água. \r\n\r\nPúblico-alvo: 9º - 12º ano, área ciências e tecnologia. Tipologia da atividade geral: mista.\r\n\r\n(a) Modelo físico e funcionamento de um aquífero\r\nEsta atividade inclui a demonstração do ciclo hidrológico e do escoamento da água no subsolo, evidenciando as particularidades da bacia hidrográfica onde nos encontramos (bacia hidrográfica das Ribeiras do Algarve) utilizando um modelo físico em corte vertical. Adicionalmente, é desenvolvida uma experiência para observação de fenómenos de infiltração e retenção de água no solo. Os alunos adicionam água a recipientes contendo diferentes tipos de solo e de cobertura. Devendo registar o tempo necessário para drenar a água até à capacidade de campo, relacionando com o tipo de solo e particularidades que alteram a sua permeabilidade e porosidade.\r\nResponsáveis: Luís Nunes e Vânia Sousa\r\nLocal: Campus de Gambelas, zonas exteriores (campo de jogos, horto e eco-circuito).\r\n\r\n(b) Monitorização de águas subterrâneas e intrusão salina\r\nEsta atividade inclui a monitorização de águas subterrâneas e a análise da intrusão salina. Utilizando o furo da Universidade do Algarve, pretende-se monitorizar a profundidade da água no furo e a qualidade da mesma através da análise de parâmetros químicos, nomeadamente pH, condutividade e nitratos, utilizando sondas de campo e tiras indicadoras. Posteriormente, diferentes percentagens de água do mar são misturadas com a água subterrânea e através da medição da condutividade elétrica é feita a relação entre os valores registados e as diferentes percentagens de mistura de água do mar Intrusão salina). \r\nResponsáveis: Luís Nunes e Vânia Sousa.\r\nLocal: Campus de Gambelas, zonas exteriores (campo de jogos, horto e eco-circuito).', 'Ciencias e Tecnologia', 7, 'Misto', 'Aceite', '2022-03-03 11:25:59.255578', '2022-03-03 12:18:40.041332', 150, 30, 3, 31, 25, 4),
(16, 'Métodos em Ciências do Mar', 'A atividade geral MÉTODOS EM CIÊNCIAS DO MAR inclui três atividades específicas integradas na área das ciências do mar: (a) Como investigamos a dinâmica litoral?; (b) Mergulho científico: ferramenta para o estudo do ambiente marinho; e (c) O mundo numa gota de água do mar: do microscópio ao satélite. Estas três atividades apresentam uma duração de 45 minutos cada e serão frequentadas, sequencialmente, por três grupos de alunos visitantes.  \r\n\r\nPúblico-alvo: 9º - 12º ano, área ciências e tecnologia. Tipologia da atividade geral: mista.\r\n\r\n(a) Como investigamos a dinâmica litoral?\r\nNesta atividade, os investigadores do Centro de Ciências do Mar e do Ambiente da Universidade do Algarve (CIMA-UAlg) discutirão com os alunos a importância das zonas costeiras, as metodologias e ferramentas utilizadas nos estudos da dinâmica do litoral e o tipo de resultados obtidos, da composição e tamanho dos sedimentos à evolução de troços costeiros baseada em imagens de satélite. Serão igualmente discutidas a utilidade e as implicações destes resultados.\r\nResponsáveis: Susana Costas, Juan Garzón e Katerina Kompiadou.\r\nLocal: Edifício 7, sala 2.57.\r\n\r\n(b) Mergulho científico: ferramenta para o estudo do ambiente marinho\r\nEsta atividade engloba vários temas e materiais pedagógicos, nomeadamente uma apresentação geral sobre o mergulho científico, vídeos curtos exemplificativos de atividades/técnicas/métodos utilizados em mergulho científico e a observação e manuseamento de equipamento de mergulho. No final, serão  apresentados cenários subaquáticos, com recurso a materiais didáticos diversos, que têm por objetivo realçar as competências requeridas para desempenhar a atividade de mergulhador científico. Destacar-se-á ainda a importância da formação técnico-científica requerida para esta atividade de mergulho, que pode ser obtida na Universidade do Algarve, e as suas saídas profissionais. \r\nResponsáveis: Duarte Duarte e Núcleo de Estudantes de Biologia e Biologia Marinha da Associação Académica da Universidade do Algarve (NEBUA).\r\nLocal: Edifício 7, sala 1.28.\r\n\r\n(c) O mundo numa gota de água do mar: do microscópio ao satélite\r\nA vida nos oceanos é riquíssima e fascinante e todos conhecemos espécies de peixes, mamíferos marinhos, e até algas e plantas marinhas, que habitam os ecossistemas marinhos. Esta atividade aborda os outros organismos marinhos, pequenos mas extremamente importantes, que não conseguimos visualizar a olho nú. A atividade inicia com uma introdução teórica sobre os microrganismos marinhos que pululam numa gota de água de mar, incluindo o fitoplâncton (microalgas), bactérias e vírus, e a sua importância nos ecossistemas. Seguidamente, serão apresentados aos alunos os métodos (ex.: deteção remota por satélite), estratégias e equipamentos utilizados para a recolha de amostras de água e medição de variáveis ambientais relevantes. Por fim, os microrganismos marinhos serão visualizados usando diferentes tipos de microscópios: o microscópio de inversão para explorar fitoplâncton e protistas fagotróficos em amostras in vivo e o microscópio de epifluorescência para observar bactérias heterotróficas e vírus planctónicos.\r\nResponsáveis: Rita Domingues, Helena Galvão e Lilian Krug.\r\nLocal: Edifício 7, laboratório 2.8.', 'Ciencias e Tecnologia', 3, 'Misto', 'Aceite', '2022-03-03 11:31:24.856034', '2022-03-03 12:18:32.858560', 180, 45, 3, 31, 25, 4),
(17, 'Ciências do Mar: organismos, ambientes e investigadores', 'A atividade geral CIÊNCIAS DO MAR: ORGANISMOS, AMBIENTES E INVESTIGADORES inclui três atividades integradas na área das ciências do mar: (a) Fitoplâncton observado sob diferentes perspetivas; (b) À descoberta de organismos gelatinosos; e (c) Quem é quem nas ciências do mar.\r\nEstas três atividades apresentam uma duração de 45 minutos cada e serão frequentadas, sequencialmente, por três grupos de alunos visitantes.  \r\n\r\nPúblico-alvo: 9º - 12º ano, área ciências e tecnologia. Tipologia da atividade geral: mista.\r\n\r\n(a) Fitoplâncton observado sob diferentes perspetivas \r\nO fitoplâncton, constituído por várias espécies de microalgas planctónicas, representa a base da rede alimentar no oceano e tem um papel fundamental na captação de dióxido de carbono da atmosfera. No entanto, algumas espécies de fitoplâncton produzem toxinas com efeitos nocivos para a saúde pública e ambiente marinho. Assim, conhecer a composição específica e distribuição do fitoplâncton nos ecossistemas marinhos é uma prioridade! Esta atividade aborda, inicialmente, o funcionamento e utilização da deteção remota por satélite para obter informação geral sobre o fitoplâncton. Contudo, para detetar a presença de espécies de fitoplâncton potencialmente nocivas, é necessário colher e analisar diretamente amostras de água. Assim, os alunos terão também oportunidade de assistir a breves demonstrações dos métodos de estudo mais convencionais, incluindo a extração de pigmentos para análise química e a utilização de microscopia para observação direta do fitoplâncton.\r\nResponsável: Sónia Cristina e Carla S. Freitas.\r\nLocal: Edifício 7, sala 1.74 e laboratórios 1.87 e 1.89.\r\n\r\n(b) À descoberta de organismos gelatinosos\r\nEsta atividade aborda a morfologia e ecologia de organismos gelatinosos integrados no Filo Cnidaria, que conhecemos no dia-a-dia por medusas. Os alunos terão oportunidade de realizar algumas atividades interativas e observar diversos organismos vivos.\r\nResponsáveis: Joana Cruz e Núcleo de Estudantes de Biologia e Biologia Marinha da Associação Académica da Universidade do Algarve (NEBUA).\r\nLocal: Edifício 7, laboratório 0.44.\r\n\r\n(c) Quem é quem nas ciências do mar\r\nNesta atividade, os alunos serão desafiados a identificar a área científica de vários investigadores com base num jogo de perguntas e respostas, com tempo limitado. Serão contempladas pelo menos quatro áreas de investigação, no âmbito das ciências do mar e do ambiente. Durante este ‘speed dating’, os investigadores apresentarão objetos representativos da sua área de investigação e estarão disponíveis para responder a perguntas chave por parte de grupos de alunos. A parte final da atividade inclui uma explanação acerca do papel do investigador na sociedade.\r\nResponsáveis: Rita Carrasco, Isabel Mendes, Lilian Krug, Rita Domingues e Margarida Vilas Boas.\r\nLocal: Edifício 7, sala 2.57.', 'Ciencias e Tecnologia', 4, 'Misto', 'Aceite', '2022-03-03 11:41:43.614545', '2022-03-03 12:18:26.976864', 180, 45, 3, 31, 25, 4),
(18, 'Fases do ciclo de vida de animais marinhos', 'A atividade geral FASES DO CICLO DE VIDA DE ANIMAIS MARINHOS inclui três atividades integradas na área da Biologia Marinha: (a) Vem explorar o interior de um peixe; (b) Como preservar espermatozoides de peixe a longo prazo?; e (c) Ciclo de vida do caranguejo: da larva ao adulto, do nativo ao invasor. Estas três atividades apresentam uma duração de 45 minutos cada e serão frequentadas, sequencialmente, por três grupos de alunos visitantes.  \r\n\r\nPúblico-alvo: 9º - 12º ano, área ciências e tecnologia. Tipologia da atividade geral: laboratorial.\r\n\r\n\r\n(a) Vem explorar o interior de um peixe \r\nEsta atividade permite aos alunos conhecerem a morfologia externa e interna de um peixe ósseo (teleósteo). Os alunos farão a disseção de um indivíduo da espécie Scomber colias, (nome vugar:  cavala) e identificarão os principais órgãos internos e as suas funções fisiológicas.\r\nResponsáveis: Teresa Modesto e Núcleo de Estudantes de Biologia e Biologia Marinha da Associação Académica da Universidade do Algarve (NEBUA).\r\nLocal: Edifício 7, laboratório 0.44.\r\n\r\n(b) Como preservar espermatozóides de peixe a longo prazo?\r\nEsta atividade demonstra como o material biológico pode ser armazenado durante anos com recurso à criopreservação. A criopreservação consiste na congelação em azoto líquido a baixas temperaturas (-196ºC). Esta atividade transmite aos alunos noções básicas de procedimentos de criopreservação, dando a conhecer os materiais e equipamentos necessários. Os alunos terão oportunidade de descongelar espermatozóides de peixes criopreservados e analisar a sua sobrevivência. Será que os espermatozóides conseguem retomar a mobilidade? \r\nResponsáveis: Elsa Cabrita, Catarina Anjos e Francisca Félix.\r\nLocal: Edifício 7, laboratório 0.44.\r\n\r\n(c) Ciclo de vida do caranguejo: da larva ao adulto, do nativo ao invasor\r\nEsta atividade iniciará com uma breve introdução ao ciclo de vida do caranguejo, com referência a espécies nativas e espécies não-nativas invasoras. Os  alunos irão visualizar as fases iniciais (larvas microscópicas planctónicas) de vida de caranguejos, com o auxílio de uma lupa binocular, bem como adultos de espécies nativas e invasoras. No final da sessão, tentarão descobrir fases larvares no estádio zoea, entre muitos outros organismos zooplanctónicos, em amostras de zooplâncton in vivo.\r\nResponsáveis: Joana Cruz e Marta Albo Puigsever\r\nLocal: Edifício 7, laboratório 0.41.', 'Ciencias e Tecnologia', 3, 'Atividade Laboratorial', 'Aceite', '2022-03-03 11:43:58.184348', '2022-03-03 12:18:19.172414', 180, 45, 3, 31, 25, 4),
(19, 'Da célula aos implantes artificiais: ciências e tecnologias', 'A atividade geral DA CÉLULA AOS IMPLANTES ARTIFICIAIS: CIÊNCIAS E TECNOLOGIAS inclui três atividades específicas integradas nas áreas da Bioquímica, Bioengenharia e Ciências da Saúde: (a) Cultura celular: aventura no multiverso da ciência; (b) A imunologia na bioquímica; e (c) Bioengenharia: o que será, como será na UAlg, e o que farei no futuro?. Estas atividades específicas apresentam uma duração de 45 minutos cada e serão frequentadas, sequencialmente, por três grupos de alunos visitantes.  \r\n\r\nPúblico-alvo: 10º - 12º ano, área ciências e tecnologia. Tipologia da atividade geral: misto.\r\n\r\n(a) Cultura celular: aventura no multiverso da ciência\r\nA cultura celular de células humanas compreende um conjunto de técnicas, que simulam as condições naturais do corpo humano, num ambiente artificial (in vitro). Tal permite-nos entender a fisiologia e bioquímica da célula e obter dados a partir de ensaios in vitro que, de outra forma, necessitariam de ser obtidos a partir de ensaios em animais (in vivo). Neste sentido, a cultura de células torna-se crucial para estudar os mecanismos biológicos, sendo utilizada em diversas áreas, principalmente na investigação fundamental, biotecnologia e medicina. A sua aplicação inclui pesquisas sobre mecanismos de doenças como o cancro, até à fabricação de vacinas, seleção e melhoria de medicamentos, terapia genética, biologia de células estaminais, tecnologia de fertilização in vitro e muito mais! Nesta atividade, os alunos vão ter oportunidade de visualizar, com recurso a microscopia de inversão, diferentes tipos de células humanas extraídas a partir de culturas celulares in vitro.\r\nResponsáveis: Dina Simes, Carla Viegas, Catarina Marreiros, Joana Carreira e Bárbara Vieira.\r\nLocal: Edifício 7, laboratório 0.41.\r\n\r\n(b) A imunologia na bioquímica\r\nA imunologia compreende uma área de investigação em Bioquímica, Biologia, Biomedicina e Medicina dedicada ao estudo dos sistemas imunológicos em organismos animais. As suas bases estão relacionadas com processos de reconhecimento celular e molecular, que definem a individualidade de cada indivíduo e o modo como cada organismo interactua com outros organismos. Esta atividade inclui o estudo do microbioma individual de alguns alunos que, por sua vez, permite compreender como é que cada pessoa interage com diversas estirpes bacterianas. \r\nResponsáveis: Deborah Power e Núcleo de Estudantes de Bioquímica da Associação Académica da Universidade do Algarve (NEBQUAL).\r\nLocal: Edifício 7, laboratório 0.32.\r\n\r\n(c) Bioengenharia: o que será, como será na UAlg e o que farei no futuro?\r\nA bioengenharia é um termo ainda pouco conhecido no vocabulário português! Até porque há muitíssimo poucos cursos em Portugal! MAS, é dos cursos mais versáteis. Quem tem gosto pela biologia, física, química, mas ainda não decidiu exatamente de qual gosta mais, pode e deve inscrever-se na licenciatura em Bioengenharia, e, decidir apenas no 3º ano se gosta mais de engenharia biomédica ou engenharia biológica. Emprego não faltará a quem tenha esta base de conhecimentos! Para melhor esclarecer o que é a bioengenharia, esta atividade desmonstrará como formamos os nossos bioengenheiros (\'o que será?\'). O Núcleo de Estudantes de Bioengenharia, recentemente criado, explicará as suas vivências enquanto alunos de bioengenharia da Universidade do Algarve (\'como será na UAlg?\'). No final, para terem idéia de \'como será no futuro?\', experienciarão o uso da tecnologia em prol de próteses clínicas.\r\nResponsáveis: Adriana Cavaco, Rui Borges, Graça Ruano e Núcleo de Estudantes de Bioengenharia da Associação Académica da Universidade do Algarve (NEB)\r\nLocal: Edifício 1, laboratório 2.76.', 'Ciencias e Tecnologia', 3, 'Misto', 'Aceite', '2022-03-03 11:48:07.781673', '2022-03-03 12:18:12.782010', 180, 45, 3, 31, 25, 4),
(21, 'Visita às Artes Visuais', 'Uma visita às instalações onde decorre a Licenciatura em Artes Visuais (AV).', 'Linguas e Humanidades', 2, 'Misto', 'Pendente', '2022-03-15 18:28:03.120040', '2022-03-15 18:29:03.741716', 30, 20, 3, 64, 37, 4),
(22, 'Teste', 'teste', 'Ciencias e Tecnologia', 1, 'Atividade Laboratorial', 'Aceite', '2023-04-19 09:31:38.903251', '2023-04-19 09:34:20.952367', 60, 45, 4, 33, 26, 4),
(23, 'Teste', 'teste', 'Ciencias e Tecnologia', 1, 'Atividade Laboratorial', 'Aceite', '2024-04-23 16:45:21.251346', '2024-04-23 16:45:21.251786', 60, 45, 6, 33, 26, 4),
(24, 'Da célula aos implantes artificiais: ciências e tecnologias', 'A atividade geral DA CÉLULA AOS IMPLANTES ARTIFICIAIS: CIÊNCIAS E TECNOLOGIAS inclui três atividades específicas integradas nas áreas da Bioquímica, Bioengenharia e Ciências da Saúde: (a) Cultura celular: aventura no multiverso da ciência; (b) A imunologia na bioquímica; e (c) Bioengenharia: o que será, como será na UAlg, e o que farei no futuro?. Estas atividades específicas apresentam uma duração de 45 minutos cada e serão frequentadas, sequencialmente, por três grupos de alunos visitantes.  \r\n\r\nPúblico-alvo: 10º - 12º ano, área ciências e tecnologia. Tipologia da atividade geral: misto.\r\n\r\n(a) Cultura celular: aventura no multiverso da ciência\r\nA cultura celular de células humanas compreende um conjunto de técnicas, que simulam as condições naturais do corpo humano, num ambiente artificial (in vitro). Tal permite-nos entender a fisiologia e bioquímica da célula e obter dados a partir de ensaios in vitro que, de outra forma, necessitariam de ser obtidos a partir de ensaios em animais (in vivo). Neste sentido, a cultura de células torna-se crucial para estudar os mecanismos biológicos, sendo utilizada em diversas áreas, principalmente na investigação fundamental, biotecnologia e medicina. A sua aplicação inclui pesquisas sobre mecanismos de doenças como o cancro, até à fabricação de vacinas, seleção e melhoria de medicamentos, terapia genética, biologia de células estaminais, tecnologia de fertilização in vitro e muito mais! Nesta atividade, os alunos vão ter oportunidade de visualizar, com recurso a microscopia de inversão, diferentes tipos de células humanas extraídas a partir de culturas celulares in vitro.\r\nResponsáveis: Dina Simes, Carla Viegas, Catarina Marreiros, Joana Carreira e Bárbara Vieira.\r\nLocal: Edifício 7, laboratório 0.41.\r\n\r\n(b) A imunologia na bioquímica\r\nA imunologia compreende uma área de investigação em Bioquímica, Biologia, Biomedicina e Medicina dedicada ao estudo dos sistemas imunológicos em organismos animais. As suas bases estão relacionadas com processos de reconhecimento celular e molecular, que definem a individualidade de cada indivíduo e o modo como cada organismo interactua com outros organismos. Esta atividade inclui o estudo do microbioma individual de alguns alunos que, por sua vez, permite compreender como é que cada pessoa interage com diversas estirpes bacterianas. \r\nResponsáveis: Deborah Power e Núcleo de Estudantes de Bioquímica da Associação Académica da Universidade do Algarve (NEBQUAL).\r\nLocal: Edifício 7, laboratório 0.32.\r\n\r\n(c) Bioengenharia: o que será, como será na UAlg e o que farei no futuro?\r\nA bioengenharia é um termo ainda pouco conhecido no vocabulário português! Até porque há muitíssimo poucos cursos em Portugal! MAS, é dos cursos mais versáteis. Quem tem gosto pela biologia, física, química, mas ainda não decidiu exatamente de qual gosta mais, pode e deve inscrever-se na licenciatura em Bioengenharia, e, decidir apenas no 3º ano se gosta mais de engenharia biomédica ou engenharia biológica. Emprego não faltará a quem tenha esta base de conhecimentos! Para melhor esclarecer o que é a bioengenharia, esta atividade desmonstrará como formamos os nossos bioengenheiros (\'o que será?\'). O Núcleo de Estudantes de Bioengenharia, recentemente criado, explicará as suas vivências enquanto alunos de bioengenharia da Universidade do Algarve (\'como será na UAlg?\'). No final, para terem idéia de \'como será no futuro?\', experienciarão o uso da tecnologia em prol de próteses clínicas.\r\nResponsáveis: Adriana Cavaco, Rui Borges, Graça Ruano e Núcleo de Estudantes de Bioengenharia da Associação Académica da Universidade do Algarve (NEB)\r\nLocal: Edifício 1, laboratório 2.76.', 'Ciencias e Tecnologia', 3, 'Misto', 'Aceite', '2024-04-23 16:45:24.684201', '2024-04-23 16:45:24.684201', 180, 45, 6, 31, 25, 4),
(25, 'Fases do ciclo de vida de animais marinhos', 'A atividade geral FASES DO CICLO DE VIDA DE ANIMAIS MARINHOS inclui três atividades integradas na área da Biologia Marinha: (a) Vem explorar o interior de um peixe; (b) Como preservar espermatozoides de peixe a longo prazo?; e (c) Ciclo de vida do caranguejo: da larva ao adulto, do nativo ao invasor. Estas três atividades apresentam uma duração de 45 minutos cada e serão frequentadas, sequencialmente, por três grupos de alunos visitantes.  \r\n\r\nPúblico-alvo: 9º - 12º ano, área ciências e tecnologia. Tipologia da atividade geral: laboratorial.\r\n\r\n\r\n(a) Vem explorar o interior de um peixe \r\nEsta atividade permite aos alunos conhecerem a morfologia externa e interna de um peixe ósseo (teleósteo). Os alunos farão a disseção de um indivíduo da espécie Scomber colias, (nome vugar:  cavala) e identificarão os principais órgãos internos e as suas funções fisiológicas.\r\nResponsáveis: Teresa Modesto e Núcleo de Estudantes de Biologia e Biologia Marinha da Associação Académica da Universidade do Algarve (NEBUA).\r\nLocal: Edifício 7, laboratório 0.44.\r\n\r\n(b) Como preservar espermatozóides de peixe a longo prazo?\r\nEsta atividade demonstra como o material biológico pode ser armazenado durante anos com recurso à criopreservação. A criopreservação consiste na congelação em azoto líquido a baixas temperaturas (-196ºC). Esta atividade transmite aos alunos noções básicas de procedimentos de criopreservação, dando a conhecer os materiais e equipamentos necessários. Os alunos terão oportunidade de descongelar espermatozóides de peixes criopreservados e analisar a sua sobrevivência. Será que os espermatozóides conseguem retomar a mobilidade? \r\nResponsáveis: Elsa Cabrita, Catarina Anjos e Francisca Félix.\r\nLocal: Edifício 7, laboratório 0.44.\r\n\r\n(c) Ciclo de vida do caranguejo: da larva ao adulto, do nativo ao invasor\r\nEsta atividade iniciará com uma breve introdução ao ciclo de vida do caranguejo, com referência a espécies nativas e espécies não-nativas invasoras. Os  alunos irão visualizar as fases iniciais (larvas microscópicas planctónicas) de vida de caranguejos, com o auxílio de uma lupa binocular, bem como adultos de espécies nativas e invasoras. No final da sessão, tentarão descobrir fases larvares no estádio zoea, entre muitos outros organismos zooplanctónicos, em amostras de zooplâncton in vivo.\r\nResponsáveis: Joana Cruz e Marta Albo Puigsever\r\nLocal: Edifício 7, laboratório 0.41.', 'Ciencias e Tecnologia', 3, 'Atividade Laboratorial', 'Aceite', '2024-04-23 16:45:28.364092', '2024-04-23 16:45:28.364092', 180, 45, 6, 31, 25, 4),
(31, 'Visita às Artes Visuais', 'Uma visita às instalações onde decorre a Licenciatura em Artes Visuais (AV).', 'Linguas e Humanidades', 2, 'Misto', 'Pendente', '2024-04-23 23:49:50.485925', '2024-04-23 23:49:50.485925', 30, 20, 6, 64, 37, 4);

-- --------------------------------------------------------

--
-- Estrutura da tabela `atividaderoteiro`
--

CREATE TABLE `atividaderoteiro` (
  `id` int(11) NOT NULL,
  `atividade_id` int(11) NOT NULL,
  `roteiro_id` int(11) NOT NULL,
  `duracao` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `atividaderoteiro`
--

INSERT INTO `atividaderoteiro` (`id`, `atividade_id`, `roteiro_id`, `duracao`) VALUES
(11, 21, 2, 120),
(12, 23, 2, 90),
(16, 24, 13, 45),
(17, 25, 13, 45),
(30, 23, 24, 45),
(31, 23, 25, 45),
(32, 25, 25, 90);

-- --------------------------------------------------------

--
-- Estrutura da tabela `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(1, 'Coordenador'),
(2, 'Participante'),
(3, 'ProfessorUniversitario'),
(4, 'Administrador'),
(5, 'Colaborador');

-- --------------------------------------------------------

--
-- Estrutura da tabela `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add permission', 1, 'add_permission'),
(2, 'Can change permission', 1, 'change_permission'),
(3, 'Can delete permission', 1, 'delete_permission'),
(4, 'Can view permission', 1, 'view_permission'),
(5, 'Can add group', 2, 'add_group'),
(6, 'Can change group', 2, 'change_group'),
(7, 'Can delete group', 2, 'delete_group'),
(8, 'Can view group', 2, 'view_group'),
(9, 'Can add user', 3, 'add_user'),
(10, 'Can change user', 3, 'change_user'),
(11, 'Can delete user', 3, 'delete_user'),
(12, 'Can view user', 3, 'view_user'),
(13, 'Can add log entry', 4, 'add_logentry'),
(14, 'Can change log entry', 4, 'change_logentry'),
(15, 'Can delete log entry', 4, 'delete_logentry'),
(16, 'Can view log entry', 4, 'view_logentry'),
(17, 'Can add anfiteatro', 5, 'add_anfiteatro'),
(18, 'Can change anfiteatro', 5, 'change_anfiteatro'),
(19, 'Can delete anfiteatro', 5, 'delete_anfiteatro'),
(20, 'Can view anfiteatro', 5, 'view_anfiteatro'),
(21, 'Can add arlivre', 6, 'add_arlivre'),
(22, 'Can change arlivre', 6, 'change_arlivre'),
(23, 'Can delete arlivre', 6, 'delete_arlivre'),
(24, 'Can view arlivre', 6, 'view_arlivre'),
(25, 'Can add atividade', 7, 'add_atividade'),
(26, 'Can change atividade', 7, 'change_atividade'),
(27, 'Can delete atividade', 7, 'delete_atividade'),
(28, 'Can view atividade', 7, 'view_atividade'),
(29, 'Can add tema', 8, 'add_tema'),
(30, 'Can change tema', 8, 'change_tema'),
(31, 'Can delete tema', 8, 'delete_tema'),
(32, 'Can view tema', 8, 'view_tema'),
(33, 'Can add sessao', 9, 'add_sessao'),
(34, 'Can change sessao', 9, 'change_sessao'),
(35, 'Can delete sessao', 9, 'delete_sessao'),
(36, 'Can view sessao', 9, 'view_sessao'),
(37, 'Can add materiais', 10, 'add_materiais'),
(38, 'Can change materiais', 10, 'change_materiais'),
(39, 'Can delete materiais', 10, 'delete_materiais'),
(40, 'Can view materiais', 10, 'view_materiais'),
(41, 'Can add preferencia', 11, 'add_preferencia'),
(42, 'Can change preferencia', 11, 'change_preferencia'),
(43, 'Can delete preferencia', 11, 'delete_preferencia'),
(44, 'Can view preferencia', 11, 'view_preferencia'),
(45, 'Can add preferencia atividade', 12, 'add_preferenciaatividade'),
(46, 'Can change preferencia atividade', 12, 'change_preferenciaatividade'),
(47, 'Can delete preferencia atividade', 12, 'delete_preferenciaatividade'),
(48, 'Can view preferencia atividade', 12, 'view_preferenciaatividade'),
(49, 'Can add colaborador horario', 13, 'add_colaboradorhorario'),
(50, 'Can change colaborador horario', 13, 'change_colaboradorhorario'),
(51, 'Can delete colaborador horario', 13, 'delete_colaboradorhorario'),
(52, 'Can view colaborador horario', 13, 'view_colaboradorhorario'),
(53, 'Can add campus', 14, 'add_campus'),
(54, 'Can change campus', 14, 'change_campus'),
(55, 'Can delete campus', 14, 'delete_campus'),
(56, 'Can view campus', 14, 'view_campus'),
(57, 'Can add curso', 15, 'add_curso'),
(58, 'Can change curso', 15, 'change_curso'),
(59, 'Can delete curso', 15, 'delete_curso'),
(60, 'Can view curso', 15, 'view_curso'),
(61, 'Can add departamento', 16, 'add_departamento'),
(62, 'Can change departamento', 16, 'change_departamento'),
(63, 'Can delete departamento', 16, 'delete_departamento'),
(64, 'Can view departamento', 16, 'view_departamento'),
(65, 'Can add diaaberto', 17, 'add_diaaberto'),
(66, 'Can change diaaberto', 17, 'change_diaaberto'),
(67, 'Can delete diaaberto', 17, 'delete_diaaberto'),
(68, 'Can view diaaberto', 17, 'view_diaaberto'),
(69, 'Can add edificio', 18, 'add_edificio'),
(70, 'Can change edificio', 18, 'change_edificio'),
(71, 'Can delete edificio', 18, 'delete_edificio'),
(72, 'Can view edificio', 18, 'view_edificio'),
(73, 'Can add espaco', 19, 'add_espaco'),
(74, 'Can change espaco', 19, 'change_espaco'),
(75, 'Can delete espaco', 19, 'delete_espaco'),
(76, 'Can view espaco', 19, 'view_espaco'),
(77, 'Can add horario', 20, 'add_horario'),
(78, 'Can change horario', 20, 'change_horario'),
(79, 'Can delete horario', 20, 'delete_horario'),
(80, 'Can view horario', 20, 'view_horario'),
(81, 'Can add menu', 21, 'add_menu'),
(82, 'Can change menu', 21, 'change_menu'),
(83, 'Can delete menu', 21, 'delete_menu'),
(84, 'Can view menu', 21, 'view_menu'),
(85, 'Can add transporte', 22, 'add_transporte'),
(86, 'Can change transporte', 22, 'change_transporte'),
(87, 'Can delete transporte', 22, 'delete_transporte'),
(88, 'Can view transporte', 22, 'view_transporte'),
(89, 'Can add transporteuniversitario', 23, 'add_transporteuniversitario'),
(90, 'Can change transporteuniversitario', 23, 'change_transporteuniversitario'),
(91, 'Can delete transporteuniversitario', 23, 'delete_transporteuniversitario'),
(92, 'Can view transporteuniversitario', 23, 'view_transporteuniversitario'),
(93, 'Can add unidadeorganica', 24, 'add_unidadeorganica'),
(94, 'Can change unidadeorganica', 24, 'change_unidadeorganica'),
(95, 'Can delete unidadeorganica', 24, 'delete_unidadeorganica'),
(96, 'Can view unidadeorganica', 24, 'view_unidadeorganica'),
(97, 'Can add transportehorario', 25, 'add_transportehorario'),
(98, 'Can change transportehorario', 25, 'change_transportehorario'),
(99, 'Can delete transportehorario', 25, 'delete_transportehorario'),
(100, 'Can view transportehorario', 25, 'view_transportehorario'),
(101, 'Can add sala', 26, 'add_sala'),
(102, 'Can change sala', 26, 'change_sala'),
(103, 'Can delete sala', 26, 'delete_sala'),
(104, 'Can view sala', 26, 'view_sala'),
(105, 'Can add prato', 27, 'add_prato'),
(106, 'Can change prato', 27, 'change_prato'),
(107, 'Can delete prato', 27, 'delete_prato'),
(108, 'Can view prato', 27, 'view_prato'),
(109, 'Can add idioma', 28, 'add_idioma'),
(110, 'Can change idioma', 28, 'change_idioma'),
(111, 'Can delete idioma', 28, 'delete_idioma'),
(112, 'Can view idioma', 28, 'view_idioma'),
(113, 'Can add tarefa', 29, 'add_tarefa'),
(114, 'Can change tarefa', 29, 'change_tarefa'),
(115, 'Can delete tarefa', 29, 'delete_tarefa'),
(116, 'Can view tarefa', 29, 'view_tarefa'),
(117, 'Can add tarefa acompanhar', 30, 'add_tarefaacompanhar'),
(118, 'Can change tarefa acompanhar', 30, 'change_tarefaacompanhar'),
(119, 'Can delete tarefa acompanhar', 30, 'delete_tarefaacompanhar'),
(120, 'Can view tarefa acompanhar', 30, 'view_tarefaacompanhar'),
(121, 'Can add tarefa outra', 31, 'add_tarefaoutra'),
(122, 'Can change tarefa outra', 31, 'change_tarefaoutra'),
(123, 'Can delete tarefa outra', 31, 'delete_tarefaoutra'),
(124, 'Can view tarefa outra', 31, 'view_tarefaoutra'),
(125, 'Can add tarefa auxiliar', 32, 'add_tarefaauxiliar'),
(126, 'Can change tarefa auxiliar', 32, 'change_tarefaauxiliar'),
(127, 'Can delete tarefa auxiliar', 32, 'delete_tarefaauxiliar'),
(128, 'Can view tarefa auxiliar', 32, 'view_tarefaauxiliar'),
(129, 'Can add escola', 33, 'add_escola'),
(130, 'Can change escola', 33, 'change_escola'),
(131, 'Can delete escola', 33, 'delete_escola'),
(132, 'Can view escola', 33, 'view_escola'),
(133, 'Can add inscricao', 34, 'add_inscricao'),
(134, 'Can change inscricao', 34, 'change_inscricao'),
(135, 'Can delete inscricao', 34, 'delete_inscricao'),
(136, 'Can view inscricao', 34, 'view_inscricao'),
(137, 'Can add responsavel', 35, 'add_responsavel'),
(138, 'Can change responsavel', 35, 'change_responsavel'),
(139, 'Can delete responsavel', 35, 'delete_responsavel'),
(140, 'Can view responsavel', 35, 'view_responsavel'),
(141, 'Can add inscricaoprato', 36, 'add_inscricaoprato'),
(142, 'Can change inscricaoprato', 36, 'change_inscricaoprato'),
(143, 'Can delete inscricaoprato', 36, 'delete_inscricaoprato'),
(144, 'Can view inscricaoprato', 36, 'view_inscricaoprato'),
(145, 'Can add inscricaotransporte', 37, 'add_inscricaotransporte'),
(146, 'Can change inscricaotransporte', 37, 'change_inscricaotransporte'),
(147, 'Can delete inscricaotransporte', 37, 'delete_inscricaotransporte'),
(148, 'Can view inscricaotransporte', 37, 'view_inscricaotransporte'),
(149, 'Can add inscricaosessao', 38, 'add_inscricaosessao'),
(150, 'Can change inscricaosessao', 38, 'change_inscricaosessao'),
(151, 'Can delete inscricaosessao', 38, 'delete_inscricaosessao'),
(152, 'Can view inscricaosessao', 38, 'view_inscricaosessao'),
(153, 'Can add informacao mensagem', 39, 'add_informacaomensagem'),
(154, 'Can change informacao mensagem', 39, 'change_informacaomensagem'),
(155, 'Can delete informacao mensagem', 39, 'delete_informacaomensagem'),
(156, 'Can view informacao mensagem', 39, 'view_informacaomensagem'),
(157, 'Can add informacao notificacao', 40, 'add_informacaonotificacao'),
(158, 'Can change informacao notificacao', 40, 'change_informacaonotificacao'),
(159, 'Can delete informacao notificacao', 40, 'delete_informacaonotificacao'),
(160, 'Can view informacao notificacao', 40, 'view_informacaonotificacao'),
(161, 'Can add notificacao', 41, 'add_notificacao'),
(162, 'Can change notificacao', 41, 'change_notificacao'),
(163, 'Can delete notificacao', 41, 'delete_notificacao'),
(164, 'Can view notificacao', 41, 'view_notificacao'),
(165, 'Can add mensagem recebida', 42, 'add_mensagemrecebida'),
(166, 'Can change mensagem recebida', 42, 'change_mensagemrecebida'),
(167, 'Can delete mensagem recebida', 42, 'delete_mensagemrecebida'),
(168, 'Can view mensagem recebida', 42, 'view_mensagemrecebida'),
(169, 'Can add mensagem enviada', 43, 'add_mensagemenviada'),
(170, 'Can change mensagem enviada', 43, 'change_mensagemenviada'),
(171, 'Can delete mensagem enviada', 43, 'delete_mensagemenviada'),
(172, 'Can view mensagem enviada', 43, 'view_mensagemenviada'),
(173, 'Can add utilizador', 44, 'add_utilizador'),
(174, 'Can change utilizador', 44, 'change_utilizador'),
(175, 'Can delete utilizador', 44, 'delete_utilizador'),
(176, 'Can view utilizador', 44, 'view_utilizador'),
(177, 'Can add administrador', 45, 'add_administrador'),
(178, 'Can change administrador', 45, 'change_administrador'),
(179, 'Can delete administrador', 45, 'delete_administrador'),
(180, 'Can view administrador', 45, 'view_administrador'),
(181, 'Can add participante', 46, 'add_participante'),
(182, 'Can change participante', 46, 'change_participante'),
(183, 'Can delete participante', 46, 'delete_participante'),
(184, 'Can view participante', 46, 'view_participante'),
(185, 'Can add professor universitario', 47, 'add_professoruniversitario'),
(186, 'Can change professor universitario', 47, 'change_professoruniversitario'),
(187, 'Can delete professor universitario', 47, 'delete_professoruniversitario'),
(188, 'Can view professor universitario', 47, 'view_professoruniversitario'),
(189, 'Can add coordenador', 48, 'add_coordenador'),
(190, 'Can change coordenador', 48, 'change_coordenador'),
(191, 'Can delete coordenador', 48, 'delete_coordenador'),
(192, 'Can view coordenador', 48, 'view_coordenador'),
(193, 'Can add colaborador', 49, 'add_colaborador'),
(194, 'Can change colaborador', 49, 'change_colaborador'),
(195, 'Can delete colaborador', 49, 'delete_colaborador'),
(196, 'Can view colaborador', 49, 'view_colaborador'),
(197, 'Can add content type', 50, 'add_contenttype'),
(198, 'Can change content type', 50, 'change_contenttype'),
(199, 'Can delete content type', 50, 'delete_contenttype'),
(200, 'Can view content type', 50, 'view_contenttype'),
(201, 'Can add session', 51, 'add_session'),
(202, 'Can change session', 51, 'change_session'),
(203, 'Can delete session', 51, 'delete_session'),
(204, 'Can view session', 51, 'view_session'),
(205, 'Can add roteiro', 52, 'add_roteiro'),
(206, 'Can change roteiro', 52, 'change_roteiro'),
(207, 'Can delete roteiro', 52, 'delete_roteiro'),
(208, 'Can view roteiro', 52, 'view_roteiro'),
(209, 'Can add atividade roteiro', 53, 'add_atividaderoteiro'),
(210, 'Can change atividade roteiro', 53, 'change_atividaderoteiro'),
(211, 'Can delete atividade roteiro', 53, 'delete_atividaderoteiro'),
(212, 'Can view atividade roteiro', 53, 'view_atividaderoteiro'),
(213, 'Can add questionario', 54, 'add_questionario'),
(214, 'Can change questionario', 54, 'change_questionario'),
(215, 'Can delete questionario', 54, 'delete_questionario'),
(216, 'Can view questionario', 54, 'view_questionario'),
(217, 'Can add pergunta', 55, 'add_pergunta'),
(218, 'Can change pergunta', 55, 'change_pergunta'),
(219, 'Can delete pergunta', 55, 'delete_pergunta'),
(220, 'Can view pergunta', 55, 'view_pergunta'),
(221, 'Can add tema questionario', 56, 'add_temaquestionario'),
(222, 'Can change tema questionario', 56, 'change_temaquestionario'),
(223, 'Can delete tema questionario', 56, 'delete_temaquestionario'),
(224, 'Can view tema questionario', 56, 'view_temaquestionario'),
(225, 'Can add opcao resposta', 57, 'add_opcaoresposta'),
(226, 'Can change opcao resposta', 57, 'change_opcaoresposta'),
(227, 'Can delete opcao resposta', 57, 'delete_opcaoresposta'),
(228, 'Can view opcao resposta', 57, 'view_opcaoresposta'),
(229, 'Can add resposta', 58, 'add_resposta'),
(230, 'Can change resposta', 58, 'change_resposta'),
(231, 'Can delete resposta', 58, 'delete_resposta'),
(232, 'Can view resposta', 58, 'view_resposta'),
(233, 'Can add estado', 59, 'add_estado'),
(234, 'Can change estado', 59, 'change_estado'),
(235, 'Can delete estado', 59, 'delete_estado'),
(236, 'Can view estado', 59, 'view_estado');

-- --------------------------------------------------------

--
-- Estrutura da tabela `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$180000$CndfyBYx78kq$fn2nYDZxJlRzXj/TJHxNUtNmGz+3U+uZQNxonAdkBnc=', '2024-05-18 12:20:15.397259', 0, 'admin', 'admin', 'admin', '', 0, 1, '2020-07-02 17:51:13.089949'),
(37, 'pbkdf2_sha256$180000$qMUZDkC7bT74$hO1cuy9aC1uyyNA4z+4VJS07rp/pDMgpRT0Y3iC1Iq0=', '2022-03-15 18:26:46.665722', 0, 'ACValente', 'António', 'Costa Valente', 'amvalente@ualg.pt', 0, 1, '2022-03-15 16:12:53.774834'),
(36, 'pbkdf2_sha256$180000$fXfbGzdLztoR$SPIaAvrm3MUc0JAeKnF1GNf5KLGaWvu8+/mFxRgOFuM=', NULL, 0, 'FCHS_DPCE', 'FCHS_DPCE', 'FCHS_DPCE', 'fcinacio@ualg.pt', 0, 1, '2022-03-15 16:03:54.936310'),
(35, 'pbkdf2_sha256$180000$49dV51bprvON$qrqCZnbP1mOiwOpmVNHUCTT1c4yWFA/4P8+Yp6FF8LI=', NULL, 0, 'atmartins', 'Ana Teresa', 'Martins', 'atmartins@ualg.pt', 0, 1, '2022-03-15 16:00:46.596487'),
(33, 'pbkdf2_sha256$180000$SEt79NjESsD1$MRRsCBHI33c0ToSyXaALvicWZT2mxbeVz9fWh1sYn9g=', '2022-03-09 14:16:47.686928', 0, 'Ivete', 'Ivete', 'Silva', 'info@ualg.pt', 0, 1, '2022-03-07 11:32:24.945600'),
(34, 'pbkdf2_sha256$180000$RRLVBkWuaSJj$kuknc9/lrW221MOGy6Ply6fEsS0roBTxcCJAuxhaqkc=', NULL, 0, 'gaborges', 'Gabriela', 'Borges', 'gaborges@ualg.pt', 0, 1, '2022-03-07 12:12:16.893732'),
(29, 'pbkdf2_sha256$180000$dFZPfkP56UxB$bZCTVS3OINMUq7cz4i9GRgkWREb6qKFjQWxmOhkaG58=', '2022-03-03 15:55:57.467222', 0, 'pscorreia@ualg.pt', 'Paula', 'Serdeira Azevedo', 'pscorreia@ualg.pt', 0, 1, '2022-02-28 12:24:09.334538'),
(31, 'pbkdf2_sha256$180000$R4VZIEMQbP6M$hXYZqt530bH9fVdA7zpkbenPc66QGkq/HsUDG9jP7gk=', '2023-04-19 09:34:11.521940', 0, 'FCT', 'FCT', 'UAlg', 'pcnvmartins@gmail.com', 0, 1, '2022-02-28 15:54:30.293608'),
(32, 'pbkdf2_sha256$180000$qGXefmH6r9DU$MmiUVWckwy1Rn+PkGnrWEEpgSwVRRNRQsvxl3yawMzo=', NULL, 0, 'pjsantos', 'Paulo Jorge', 'Maia dos Santos', 'pjsantos@ualg.pt', 0, 1, '2022-03-02 16:10:57.022054'),
(23, 'pbkdf2_sha256$180000$V7gVHaiKyGRP$71/B2Aye/lXWt5t9wz6GPfMwgOMeVQziCZAKCD4JK10=', '2022-03-09 14:58:30.221368', 0, 'isilva@ualg.pt', 'Ivete', 'Silva', 'isilva@ualg.pt', 0, 1, '2022-02-16 10:29:29.616641'),
(28, 'pbkdf2_sha256$180000$fqAYuNPoBL4u$qty1h/oaPLWcXJF2aABoRdOEn9LlYa0KqEl2Q+vnvms=', NULL, 0, 'Eugénia', 'Eugénia', 'Ferreira', 'ecastela@ualg.pt', 0, 1, '2022-02-26 10:23:20.418581'),
(26, 'pbkdf2_sha256$180000$33IEgNRRtfv0$A5AwJGg+FUfZ/ebyyyMCMD96KoL9o4Tv+ngG4ypryNs=', '2023-09-25 11:18:56.017870', 0, 'pventura', 'Paula', 'Ventura Martins', 'pventura@ualg.pt', 0, 1, '2022-02-23 19:00:39.878596'),
(25, 'pbkdf2_sha256$180000$k9gGmvn6aEZY$Tm4WrwB7mh3c7ROzJw/pFYpQuMLj8z0l8L2vdk9sY2g=', '2022-03-03 12:06:40.973125', 0, 'abarbosa', 'Ana', 'Barbosa', 'abarbosa@ualg.pt', 0, 1, '2022-02-23 15:57:06.463555'),
(38, 'pbkdf2_sha256$180000$wAdQrymWmQdU$eyivk8VWwKS/1wvwFSVvFGOGAeWJ6zbF4X/DFjjlPg4=', '2023-04-19 09:39:43.745415', 0, 'pventura2', 'Paula', 'Martins', 'pcnvmartins1@gmail.com', 0, 1, '2022-04-21 14:46:51.545381'),
(39, 'pbkdf2_sha256$180000$5bTnUTTHcrxy$Abzg/VzK41cDJYLsH7awlFw2uURDDhK14Nxbp9KZsI4=', NULL, 0, 'mz', 'Marielba', 'Zacarias', 'mz@ualg.pt', 0, 1, '2023-05-18 16:13:25.030743'),
(40, 'pbkdf2_sha256$180000$wNmJbmhBftQ2$KtzVc0KYrKw3BEL+EUF4mECBrHD7VvOw4AtKKV0eTyQ=', '2023-11-06 12:49:38.293446', 0, 'AMS', 'AMS', 'AMS', 'ams@ualg.pt', 0, 1, '2023-09-25 11:05:59.657572'),
(41, 'pbkdf2_sha256$180000$bSQkyvxCz5JY$8E2SQFs4nxEuOelI6IfxgQOa6AaWmy6FM7zUMeleY3o=', '2024-05-16 10:08:36.293337', 0, 'olajohn', 'Ola', 'John', 'ola@ola.pt', 0, 1, '2024-04-23 16:42:11.689049');

-- --------------------------------------------------------

--
-- Estrutura da tabela `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `auth_user_groups`
--

INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(1, 1, 4),
(39, 38, 2),
(38, 37, 3),
(37, 36, 1),
(36, 35, 3),
(35, 34, 1),
(34, 33, 2),
(32, 32, 1),
(29, 29, 1),
(31, 31, 1),
(23, 23, 4),
(28, 28, 1),
(26, 26, 3),
(25, 25, 3),
(40, 39, 3),
(41, 40, 2),
(42, 41, 1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `campus`
--

CREATE TABLE `campus` (
  `ID` int(11) NOT NULL,
  `Nome` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `campus`
--

INSERT INTO `campus` (`ID`, `Nome`) VALUES
(1, 'Penha'),
(2, 'Gambelas'),
(3, 'Portimao');

-- --------------------------------------------------------

--
-- Estrutura da tabela `colaborador`
--

CREATE TABLE `colaborador` (
  `utilizador_ptr_id` int(11) NOT NULL,
  `curso_id` int(11) NOT NULL,
  `departamento_id` int(11) NOT NULL,
  `faculdade_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `colaboradorhorario`
--

CREATE TABLE `colaboradorhorario` (
  `ID` int(11) NOT NULL,
  `dia` date NOT NULL,
  `Inicio` time(6) NOT NULL,
  `Fim` time(6) NOT NULL,
  `ColaboradorUtilizadorID` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `coordenador`
--

CREATE TABLE `coordenador` (
  `utilizador_ptr_id` int(11) NOT NULL,
  `Gabinete` varchar(255) NOT NULL,
  `DepartamentoID` int(11) NOT NULL,
  `FaculdadeID` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `coordenador`
--

INSERT INTO `coordenador` (`utilizador_ptr_id`, `Gabinete`, `DepartamentoID`, `FaculdadeID`) VALUES
(29, '33', 5, 2),
(28, '2.55', 18, 7),
(31, 'Ed. 1 2.69', 21, 6),
(32, 'Direção', 9, 4),
(34, '84', 2, 1),
(36, '1.32', 20, 5),
(41, '111', 21, 6);

-- --------------------------------------------------------

--
-- Estrutura da tabela `curso`
--

CREATE TABLE `curso` (
  `ID` int(11) NOT NULL,
  `Nome` varchar(255) DEFAULT NULL,
  `Sigla` varchar(32) DEFAULT NULL,
  `Unidadeorganica` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `curso`
--

INSERT INTO `curso` (`ID`, `Nome`, `Sigla`, `Unidadeorganica`) VALUES
(1, 'Ciências da Comunicação (Lic.)', 'LCC', 1),
(2, 'Design de Comunicação (Lic.)', 'LDC', 1),
(3, 'Desporto (Lic.)', 'LDesp', 1),
(4, 'Educação Básica (Lic.)', 'LEB', 1),
(5, 'Educação Social (Lic.)', 'LES', 1),
(6, 'Imagem Animada (Lic.)', 'LIA', 1),
(7, 'Gestão (Lic.)', 'LG', 2),
(8, 'Gestão Hoteleira (Lic.)', 'LGH', 2),
(9, 'Marketing (Lic.)', 'LMark', 2),
(10, 'Turismo (Lic.)', 'LT', 2),
(11, 'Bioengenharia (Lic.)', 'LBioeng', 6),
(12, 'Ciências Biomédicas Laboratoriais (Lic.)', 'LCBL', 3),
(13, 'Dietética e Nutrição (Lic.)', 'LDN', 3),
(14, 'Enfermagem (Lic.)', 'LEnf', 3),
(15, 'Farmácia (Lic.)', 'LFarm', 3),
(16, 'Imagem Médica e Radioterapia (Lic.)', 'LIMR', 3),
(19, 'Engenharia Alimentar (Lic.)', 'LEA', 4),
(20, 'Engenharia Civil (Lic.)', 'LEC', 4),
(21, 'Engenharia Eletrotécnica e de Computadores (Lic.)', 'LEEC', 4),
(22, 'Engenharia Mecânica (Lic.)', 'LEM', 4),
(48, 'Design e Tecnologias Multimédia (CTeSP)', 'CTeSPDTM', 1),
(55, 'Construção Civil (CTeSP)', 'CTeSPCC', 4),
(25, 'Artes Visuais (Lic.)', 'LAV', 5),
(26, 'Ciências da Educação e da Formação (Lic.)', 'LCEF', 5),
(27, 'Línguas e Comunicação (Lic.)', 'LLC', 5),
(28, 'Línguas, Literaturas e Culturas (Lic.)', 'LLLC', 5),
(29, 'Património Cultural e Arqueologia (Lic.)', 'LPCA', 5),
(30, 'Psicologia (Lic.)', 'LPsic', 5),
(31, 'Agronomia (Lic.)', 'LAgr', 6),
(32, 'Arquitetura Paisagista (Lic.)', 'LAP', 6),
(63, 'Biotecnologia (Lic.)', 'LBiotec', 6),
(34, 'Biologia (Lic.)', 'LBiol', 6),
(35, 'Biologia Marinha (Lic.)', 'LBM', 6),
(36, 'Bioquímica (Lic.)', 'LBioq', 6),
(38, 'Engenharia Informática (Lic.)', 'LEI', 6),
(39, 'Gestão Marinha e Costeira (Lic.)', 'LGMC', 6),
(40, 'Matemática Aplicada à Economia e à Gestão (Lic.)', 'LMAEG', 6),
(41, 'Ciências Farmacêuticas (MI)', 'MICF', 6),
(42, 'Economia (Lic.)', 'LEcon', 7),
(43, 'Gestão de Empresas (Lic.)', 'LGE', 7),
(44, 'Sociologia (Lic.)', 'LSoc', 7),
(45, 'Ciências Biomédicas (Lic.)', 'LCB', 8),
(46, 'Medicina (MI)', 'MIM', 8),
(49, 'Contabilidade (CTeSP)', 'CTeSPCont', 2),
(50, 'Gestão de Animação Turística (CTeSP)', 'CTeSPGAT', 2),
(51, 'Marketing Digital (CTeSP)', 'CTeSPMD', 2),
(52, 'Secretariado Executivo (CTeSP)', 'CTeSPSE', 2),
(53, 'Sistemas e Tecnologias de Informação (CTeSP)', 'CTeSPSTI', 2),
(54, 'Fisioterapia (Lic.)', 'LFisiot', 3),
(56, 'Desenho e Modelação Digital (CTeSP)', 'CTeSPDMD', 4),
(57, 'Inovação e Qualidade Alimentar (CTeSP)', 'CTeSPIQA', 4),
(58, 'Instalações Elétricas, Domótica e Automação (CTeSP)', 'CTeSPIEDA', 4),
(59, 'Segurança e Higiene Alimentar (CTeSP)', 'CTeSPSHA', 4),
(60, 'Sistemas e Tecnologias de Informação (CTeSP)', 'CTeSPSTI', 4),
(61, 'Tecnologia e Manutenção Automóvel (CTeSP)', 'CTeSPTMA', 4),
(62, 'Tecnologias Informáticas (CTeSP)', 'CTeSPTI', 4);

-- --------------------------------------------------------

--
-- Estrutura da tabela `departamento`
--

CREATE TABLE `departamento` (
  `ID` int(11) NOT NULL,
  `Nome` varchar(255) DEFAULT NULL,
  `Sigla` varchar(32) DEFAULT NULL,
  `UnidadeOrganicaID` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `departamento`
--

INSERT INTO `departamento` (`ID`, `Nome`, `Sigla`, `UnidadeOrganicaID`) VALUES
(1, 'Ciências Sociais e da Educação', 'CSE', 1),
(2, 'Comunicação, Artes e Design', 'CAD', 1),
(3, 'Línguas, Literaturas e Culturas', 'LLC', 1),
(4, 'Ciências Exatas, Naturais e Desporto', 'CEND', 1),
(5, 'Escola Superior de Gestão Hotelaria e Turismo', 'ESGHT', 2),
(6, 'Escola Superior de Saúde', 'ESS', 3),
(7, 'Engenharia Alimentar', 'EA', 4),
(8, 'Engenharia Civil', 'EC', 4),
(9, 'Engenharia Eletrotécnica', 'EE', 4),
(10, 'Engenharia Mecânica', 'EM', 4),
(20, 'Psicologia e Ciências da Educação', 'DPCE', 5),
(11, 'Artes e Humanidades', 'DAH', 5),
(12, 'Ciências Biológicas e Bioengenharia', 'DCBB', 6),
(13, 'Ciências da Terra, do Mar e do Ambiente', 'DCTMA', 6),
(14, 'Engenharia Eletrónica e Informática', 'DEEI', 6),
(15, 'Física', 'DF', 6),
(16, 'Matemática', 'DM', 6),
(17, 'Química e Farmácia', 'DQF', 6),
(18, 'Faculdade de Economia', 'FE', 7),
(19, 'Faculdade de Medicina e Ciências Biomédicas', 'FMCB', 8),
(21, 'FCT', 'FCT', 6),
(22, 'Desporto Penha', 'DP', 9),
(23, 'Desporto Gambelas', 'DG', 10),
(24, 'Escola Superior de Educação e Comunicação', 'ESEC', 1),
(25, 'Instituto Superior de Engenharia', 'ISE', 4),
(26, 'Faculdade de Ciências Humanas e Sociais', 'FCHS', 5),
(27, 'Medicina', 'MIM', 8),
(28, 'Ciências Biomédicas', 'CB', 8),
(29, 'Biblioteca Penha', 'BP', 11),
(30, 'Biblioteca Gambelas', 'BG', 12),
(31, 'Gabinete de Comunicação e Protocolo', 'GCP', 13);

-- --------------------------------------------------------

--
-- Estrutura da tabela `diaaberto`
--

CREATE TABLE `diaaberto` (
  `PrecoAlunos` double NOT NULL,
  `PrecoProfessores` double DEFAULT NULL,
  `ID` int(11) NOT NULL,
  `EnderecoPaginaWeb` varchar(255) NOT NULL,
  `Descricao` longtext NOT NULL,
  `EmailDiaAberto` varchar(255) NOT NULL,
  `Ano` int(11) NOT NULL,
  `DataDiaAbertoInicio` datetime(6) NOT NULL,
  `DataDiaAbertoFim` datetime(6) NOT NULL,
  `DataInscricaoAtividadesInicio` datetime(6) NOT NULL,
  `DataInscricaoAtividadesFim` datetime(6) NOT NULL,
  `DataPropostasAtividadesIncio` datetime(6) NOT NULL,
  `DataPorpostaAtividadesFim` datetime(6) NOT NULL,
  `EscalaSessoes` time(6) NOT NULL,
  `AdministradorUtilizadorID` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `diaaberto`
--

INSERT INTO `diaaberto` (`PrecoAlunos`, `PrecoProfessores`, `ID`, `EnderecoPaginaWeb`, `Descricao`, `EmailDiaAberto`, `Ano`, `DataDiaAbertoInicio`, `DataDiaAbertoFim`, `DataInscricaoAtividadesInicio`, `DataInscricaoAtividadesFim`, `DataPropostasAtividadesIncio`, `DataPorpostaAtividadesFim`, `EscalaSessoes`, `AdministradorUtilizadorID`) VALUES
(2.85, 4.7, 3, 'Dia Aberto 2022', 'Nos dias 3 e 4 de maio de 2022, a Universidade do Algarve estará de portas abertas para toda a comunidade.\r\n\r\n A iniciativa é destinada a alunos dos 9.º, 10.º, 11.º e 12.º anos e seus professores, bem como a encarregados de educação, outros agentes educativos e demais interessados. \r\n\r\nCom o objetivo de divulgar a oferta formativa para o próximo ano letivo e dar a conhecer o trabalho pedagógico e científico desenvolvido na UAlg, o Dia Aberto 2022 apresenta um programa variado, com iniciativas de carácter informativo, pedagógico, experimental e até lúdico, onde se incluem atividades experimentais, palestras e workshops, visitas guiadas, exposições e atividades desportivas.', 'diaaberto@ualg.pt', 2022, '2022-05-03 08:30:00.000000', '2022-05-04 18:00:00.000000', '2021-03-21 23:55:00.000000', '2022-04-29 23:55:00.000000', '2022-02-15 23:55:00.000000', '2022-03-20 23:55:00.000000', '00:30:00.000000', 23),
(2.9, 4.35, 4, 'https://www.ualg.pt/inscricoes-abertas-para-os-dias-abertos-da-ualg', 'Com o objetivo de divulgar a oferta formativa e dar a conhecer o trabalho pedagógico e científico desenvolvido na Universidade do Algarve, o Dia Aberto apresenta um programa variado com atividades de carácter informativo, pedagógico, experimental e lúdico. ​​​​​​​\r\n\r\nPúblico-Alvo\r\n\r\nA iniciativa é destinada aos alunos dos 9.º, 10.º, 11.º e 12.º anos e aos seus professores, mas também outros agentes educativos, procurando incluir os encarregados de educação e demais cidadãos interessados.\r\n\r\nData\r\n\r\nEm 2023, a iniciativa vai realizar-se nos dias 18 e 19 de abril.\r\n\r\nInscrição\r\n\r\nO formulário de inscrição online está disponível até 31 de março.\r\n\r\nNota: login: escolas | password: escolas\r\n\r\nPrograma\r\n\r\nO programa contempla iniciativas variadas nos 2 campi (Penha e Gambelas), onde se realizarão atividades experimentais, palestras e workshops, visitas guiadas, exposições e atividades desportivas.\r\n\r\n18 de abril disponível aqui\r\n19 de abril disponível aqui\r\nTransportes\r\n\r\nOs grupos visitantes devem organizar o seu transporte até Faro.\r\n\r\nAutocarro camarário/de aluguer Os grupos que se fizerem transportar em autocarro próprio deverão, na chegada, dirigir-se à receção do campus onde se realizará a primeira atividade do seu programa para receber o kit de boas-vindas. Os percursos entre campi deverão ser organizados utilizando os seus autocarros.  \r\nComboio Os grupos que se fizerem transportar de comboio até à estação da CP em Faro utilizarão, a partir daí, os autocarros disponibilizados pela Universidade do Algarve para circularem entre os campi. Prevendo-se um significativo aumento de passageiros neste dia, solicita-se aos grupos que contactem antecipadamente a CP, através do email gruposlc-rg@cp.pt para a reserva de bilhetes. Desta forma, poderão beneficiar de tarifas bonificadas para grupos, com descontos entre 10% e 30% (dependendo da distância percorrida).  \r\nTransporte público rodoviário Os grupos que se fizerem transportar de autocarro público deverão sair na estação terminal, em Faro. Utilizarão, a partir daí, os autocarros disponibilizados pela Universidade do Algarve.  \r\nOutros meios Os grupos que se façam transportar por outros meios (a pé, transporte próprio) deverão, na chegada, dirigir-se à receção do campus onde se realizará a primeira atividade do seu programa para receber o kit de boas-vindas. Os percursos entre campi poderão ser assegurados pelos autocarros disponibilizados pela Universidade do Algarve. Para tal, deverão assinalar, no formulário, que “precisam de “transporte para efetuar as visitas entre os 2 campi”.\r\nRefeições\r\n\r\nOs alunos e professores que desejarem almoçar nas cantinas universitárias devem mencioná-lo no formulário de inscrição.\r\nO preço da refeição é de 2,90 Euros para estudantes e de 4,35 Euros para docentes e acompanhantes e as senhas deverão ser levantadas no dia da visita.', 'diaaberto2021@ualg.pt', 2023, '2023-12-06 09:00:00.000000', '2023-12-07 17:00:00.000000', '2023-11-06 10:36:00.000000', '2023-11-16 23:55:00.000000', '2023-03-06 23:55:00.000000', '2023-04-18 10:35:00.000000', '00:30:00.000000', 1),
(0.01, 0.01, 6, 'UAlg Gambelas', 'TESTE 2024', 'pedromartins-00@hotmail.com', 2024, '2024-06-29 11:00:00.000000', '2024-06-30 16:53:00.000000', '2024-05-10 23:55:00.000000', '2024-05-31 23:55:00.000000', '2024-04-22 23:55:00.000000', '2024-05-22 23:55:00.000000', '00:44:00.000000', 1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'auth', 'permission'),
(2, 'auth', 'group'),
(3, 'auth', 'user'),
(4, 'admin', 'logentry'),
(5, 'atividades', 'anfiteatro'),
(6, 'atividades', 'arlivre'),
(7, 'atividades', 'atividade'),
(8, 'atividades', 'tema'),
(9, 'atividades', 'sessao'),
(10, 'atividades', 'materiais'),
(11, 'colaboradores', 'preferencia'),
(12, 'colaboradores', 'preferenciaatividade'),
(13, 'colaboradores', 'colaboradorhorario'),
(14, 'configuracao', 'campus'),
(15, 'configuracao', 'curso'),
(16, 'configuracao', 'departamento'),
(17, 'configuracao', 'diaaberto'),
(18, 'configuracao', 'edificio'),
(19, 'configuracao', 'espaco'),
(20, 'configuracao', 'horario'),
(21, 'configuracao', 'menu'),
(22, 'configuracao', 'transporte'),
(23, 'configuracao', 'transporteuniversitario'),
(24, 'configuracao', 'unidadeorganica'),
(25, 'configuracao', 'transportehorario'),
(26, 'configuracao', 'sala'),
(27, 'configuracao', 'prato'),
(28, 'configuracao', 'idioma'),
(29, 'coordenadores', 'tarefa'),
(30, 'coordenadores', 'tarefaacompanhar'),
(31, 'coordenadores', 'tarefaoutra'),
(32, 'coordenadores', 'tarefaauxiliar'),
(33, 'inscricoes', 'escola'),
(34, 'inscricoes', 'inscricao'),
(35, 'inscricoes', 'responsavel'),
(36, 'inscricoes', 'inscricaoprato'),
(37, 'inscricoes', 'inscricaotransporte'),
(38, 'inscricoes', 'inscricaosessao'),
(39, 'notificacoes', 'informacaomensagem'),
(40, 'notificacoes', 'informacaonotificacao'),
(41, 'notificacoes', 'notificacao'),
(42, 'notificacoes', 'mensagemrecebida'),
(43, 'notificacoes', 'mensagemenviada'),
(44, 'utilizadores', 'utilizador'),
(45, 'utilizadores', 'administrador'),
(46, 'utilizadores', 'participante'),
(47, 'utilizadores', 'professoruniversitario'),
(48, 'utilizadores', 'coordenador'),
(49, 'utilizadores', 'colaborador'),
(50, 'contenttypes', 'contenttype'),
(51, 'sessions', 'session'),
(52, 'atividades', 'roteiro'),
(53, 'atividades', 'atividaderoteiro'),
(54, 'questionario', 'questionario'),
(55, 'questionario', 'pergunta'),
(56, 'questionario', 'temaquestionario'),
(57, 'questionario', 'opcaoresposta'),
(58, 'questionario', 'resposta'),
(59, 'questionario', 'estado');

-- --------------------------------------------------------

--
-- Estrutura da tabela `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2020-07-02 17:49:38.401669'),
(2, 'auth', '0001_initial', '2020-07-02 17:49:39.089180'),
(3, 'admin', '0001_initial', '2020-07-02 17:49:39.594901'),
(4, 'admin', '0002_logentry_remove_auto_add', '2020-07-02 17:49:39.735522'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2020-07-02 17:49:39.751149'),
(6, 'configuracao', '0001_initial', '2020-07-02 17:49:40.823253'),
(7, 'contenttypes', '0002_remove_content_type_name', '2020-07-02 17:49:41.570640'),
(8, 'auth', '0002_alter_permission_name_max_length', '2020-07-02 17:49:41.601878'),
(9, 'auth', '0003_alter_user_email_max_length', '2020-07-02 17:49:41.633125'),
(10, 'auth', '0004_alter_user_username_opts', '2020-07-02 17:49:41.648754'),
(11, 'auth', '0005_alter_user_last_login_null', '2020-07-02 17:49:41.695626'),
(12, 'auth', '0006_require_contenttypes_0002', '2020-07-02 17:49:41.695626'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2020-07-02 17:49:41.695626'),
(14, 'auth', '0008_alter_user_username_max_length', '2020-07-02 17:49:41.742501'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2020-07-02 17:49:41.773752'),
(16, 'auth', '0010_alter_group_name_max_length', '2020-07-02 17:49:41.805002'),
(17, 'auth', '0011_update_proxy_permissions', '2020-07-02 17:49:41.836252'),
(18, 'utilizadores', '0001_initial', '2020-07-02 17:49:42.226887'),
(19, 'configuracao', '0002_auto_20200702_1848', '2020-07-02 17:49:42.917702'),
(20, 'configuracao', '0003_auto_20200702_1848', '2020-07-02 17:49:42.995828'),
(21, 'atividades', '0001_initial', '2020-07-02 17:49:43.721253'),
(22, 'colaboradores', '0001_initial', '2020-07-02 17:49:44.158759'),
(23, 'configuracao', '0004_auto_20200702_1848', '2020-07-02 17:49:44.445351'),
(24, 'configuracao', '0005_auto_20200702_1848', '2020-07-02 17:49:44.460973'),
(25, 'inscricoes', '0001_initial', '2020-07-02 17:49:44.895467'),
(26, 'coordenadores', '0001_initial', '2020-07-02 17:49:45.777026'),
(27, 'coordenadores', '0002_tarefaacompanhar_inscricao', '2020-07-02 17:49:46.105154'),
(28, 'notificacoes', '0001_initial', '2020-07-02 17:49:46.387837'),
(29, 'notificacoes', '0002_auto_20200702_1848', '2020-07-02 17:49:47.271825'),
(30, 'notifications', '0001_initial', '2020-07-02 17:49:47.365577'),
(31, 'notifications', '0002_auto_20150224_1134', '2020-07-02 17:49:47.477078'),
(32, 'notifications', '0003_notification_data', '2020-07-02 17:49:47.504081'),
(33, 'notifications', '0004_auto_20150826_1508', '2020-07-02 17:49:47.519713'),
(34, 'notifications', '0005_auto_20160504_1520', '2020-07-02 17:49:47.535336'),
(35, 'notifications', '0006_indexes', '2020-07-02 17:49:47.582213'),
(36, 'notifications', '0007_add_timestamp_index', '2020-07-02 17:49:47.597840'),
(37, 'notifications', '0008_index_together_recipient_unread', '2020-07-02 17:49:47.613464'),
(38, 'sessions', '0001_initial', '2020-07-02 17:49:47.722842'),
(39, 'configuracao', '0006_auto_20240315_1127', '2024-04-23 16:17:20.594294'),
(40, 'configuracao', '0007_auto_20240315_1216', '2024-04-23 16:17:20.609948'),
(41, 'configuracao', '0008_auto_20240315_1254', '2024-04-23 16:17:20.625569'),
(42, 'configuracao', '0009_auto_20240316_1817', '2024-04-23 16:17:20.625569'),
(43, 'configuracao', '0010_auto_20240316_1820', '2024-04-23 16:17:20.641202'),
(44, 'configuracao', '0011_auto_20240316_1821', '2024-04-23 16:17:20.656783'),
(45, 'configuracao', '0012_auto_20240413_1257', '2024-04-23 16:17:20.656783'),
(46, 'configuracao', '0013_auto_20240413_1557', '2024-04-23 16:17:20.672440'),
(47, 'configuracao', '0014_auto_20240415_0011', '2024-04-23 16:17:20.672440'),
(48, 'configuracao', '0015_auto_20240415_0012', '2024-04-23 16:17:20.688020'),
(49, 'configuracao', '0016_auto_20240415_0150', '2024-04-23 16:17:20.703641'),
(50, 'configuracao', '0017_auto_20240415_0208', '2024-04-23 16:17:20.703641'),
(51, 'atividades', '0002_auto_20240415_0208', '2024-04-23 16:17:21.493950'),
(52, 'atividades', '0003_auto_20240423_1717', '2024-04-23 16:17:59.618715'),
(53, 'configuracao', '0018_auto_20240418_1919', '2024-04-23 16:17:59.696821'),
(54, 'questionario', '0001_initial', '2024-04-23 16:18:00.556344'),
(55, 'questionario', '0002_auto_20240419_1149', '2024-04-23 16:19:03.801993'),
(56, 'questionario', '0003_auto_20240518_1343', '2024-05-18 12:43:59.259414'),
(57, 'inscricoes', '0002_auto_20240518_1421', '2024-05-18 13:21:55.673701'),
(58, 'atividades', '0004_sessao_nr_presentes', '2024-05-18 13:24:02.329992');

-- --------------------------------------------------------

--
-- Estrutura da tabela `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('fhkfe4zpv803deh44qzmstr36nphox6c', 'ZjgwZjEwMDc1OGU4YWRmODA1Y2JiMGFiZDJjZWY1OTRmMjNjZjcwODp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4MWY4NTZkMjI1YWM5YjBkMGU0YmE5NDY2NTJjMDljZDNkZjY3M2RhIn0=', '2020-07-16 18:30:40.901947'),
('rdxi43aa30z2nl8zhxi26o9pjdy0oe3l', 'YmY5YmMwYTExNjU3NzcwYTU0MTAwMmUzODRlNWJkZWU0M2U5NjJhZjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzZjZmMjU1NDZkYTg4ZjI5NGRhNDkzYzRiMzNhNGJjNjliYmQ4Y2JlIn0=', '2020-07-23 09:47:31.544377'),
('0s28k1k8i9fyg90cod172nxfkct6zkov', 'YmY5YmMwYTExNjU3NzcwYTU0MTAwMmUzODRlNWJkZWU0M2U5NjJhZjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzZjZmMjU1NDZkYTg4ZjI5NGRhNDkzYzRiMzNhNGJjNjliYmQ4Y2JlIn0=', '2020-07-23 10:44:55.754762'),
('doadp7hfvlm766toscguymzczmdlti9j', 'YmY5YmMwYTExNjU3NzcwYTU0MTAwMmUzODRlNWJkZWU0M2U5NjJhZjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzZjZmMjU1NDZkYTg4ZjI5NGRhNDkzYzRiMzNhNGJjNjliYmQ4Y2JlIn0=', '2021-03-12 01:14:54.938284'),
('wekq299jz9rrl6ttrd50o5dgtbpd2wro', 'YmY5YmMwYTExNjU3NzcwYTU0MTAwMmUzODRlNWJkZWU0M2U5NjJhZjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzZjZmMjU1NDZkYTg4ZjI5NGRhNDkzYzRiMzNhNGJjNjliYmQ4Y2JlIn0=', '2021-03-15 16:04:23.332253'),
('5jfswg6ro2vh9q9uzhgphpwst0fxjzuu', 'ZWZhMDgyNDhlYzRjNzFjMjczNjZlMmY2NGFkZmViYjA1NThiZTdkYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlZDhkNDM0NzNiZTkzMzM5NjQzMDBlZTA1ODc4MGJlOWQyNDEyNmU3In0=', '2021-05-13 09:47:28.870244'),
('wr2vzm4panz54k78pbzdd7vi8ef8eg8e', 'ZWZhMDgyNDhlYzRjNzFjMjczNjZlMmY2NGFkZmViYjA1NThiZTdkYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlZDhkNDM0NzNiZTkzMzM5NjQzMDBlZTA1ODc4MGJlOWQyNDEyNmU3In0=', '2021-05-19 13:46:49.474672'),
('rhpjhoayrot9g5n3bausr9wmm311jgr7', 'NDA0YTAzZDg4Mzg4YzBkOThlNjIzNmM5NzQ5YmU3MmE1ZGRkNmVhMDp7Il9hdXRoX3VzZXJfaWQiOiIxNiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYzFlMTg0ODFmYzlhODY0ZTUxMjkwYmIxNmRjZTdiNTcxZTRiMzFmMCIsIndpemFyZF9jcmlhcl9pbnNjcmljYW8iOnsic3RlcCI6ImluZm8iLCJzdGVwX2RhdGEiOnt9LCJzdGVwX2ZpbGVzIjp7fSwiZXh0cmFfZGF0YSI6e319fQ==', '2021-05-19 14:14:36.647300'),
('599m86ourma7s4dx9doexp6dkq1ru5ck', 'ODFiYWJmZDJlMjdmYTRmYTYwOWExYzU5NmZiODhlNDc4OTQ0YTBmODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlZDhkNDM0NzNiZTkzMzM5NjQzMDBlZTA1ODc4MGJlOWQyNDEyNmU3IiwiY29uc3VsdGFyX3V0aWxpemFkb3JlcyI6Imh0dHA6Ly8xMC40LjAuOTg6ODU4NS91dGlsaXphZG9yZXMvY29uc3VsdGFydXRpbGl6YWRvcmVzP3BhZ2U9MiJ9', '2021-05-28 14:02:14.438656'),
('byhigg58b9jy0cl7jvjrb64kwo3at4gl', 'ZWZhMDgyNDhlYzRjNzFjMjczNjZlMmY2NGFkZmViYjA1NThiZTdkYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlZDhkNDM0NzNiZTkzMzM5NjQzMDBlZTA1ODc4MGJlOWQyNDEyNmU3In0=', '2021-06-09 13:39:17.694431'),
('6xwh2n4wshlwbret020ecl1fa1evdbrj', 'NWQ2MDA3MWI3NzZhMWY1NmM0MjViZjBkNzZlZTZjZWQzOTU0MzUzYTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlZDhkNDM0NzNiZTkzMzM5NjQzMDBlZTA1ODc4MGJlOWQyNDEyNmU3IiwiY29uc3VsdGFyX3V0aWxpemFkb3JlcyI6Imh0dHA6Ly8xMC40LjAuOTg6ODU4NS91dGlsaXphZG9yZXMvY29uc3VsdGFydXRpbGl6YWRvcmVzIn0=', '2021-06-25 14:55:27.979532'),
('4ql2uq975u011vc2gtgd4g1pmy1fjcti', 'ZWZhMDgyNDhlYzRjNzFjMjczNjZlMmY2NGFkZmViYjA1NThiZTdkYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlZDhkNDM0NzNiZTkzMzM5NjQzMDBlZTA1ODc4MGJlOWQyNDEyNmU3In0=', '2022-02-22 15:36:04.859925'),
('9exuci7qb3uqlwlrvqupecovmbgk5khl', 'ODFiYjc2ZmI3NTYzYjYxM2E5NGYzMTAyZjMzNzBjMWJmNWUyZTE0YTp7Il9hdXRoX3VzZXJfaWQiOiIyNiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiM2MxMmNlZjk0NGFiZTFkZTI4NTA4YWQ5MWJkNmJlNTQ1NjM0MjM1NyJ9', '2022-03-14 16:26:27.679442'),
('5wfu21fsfl7x0jhep2mo9xwd3ky3q0dc', 'ZWZhMDgyNDhlYzRjNzFjMjczNjZlMmY2NGFkZmViYjA1NThiZTdkYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlZDhkNDM0NzNiZTkzMzM5NjQzMDBlZTA1ODc4MGJlOWQyNDEyNmU3In0=', '2022-03-09 19:08:29.598267'),
('so14fnqckknmvdtnofrc6zu7gdsp6zbd', 'NTFiZjg5MjY4ZTU3ZWEzNjg4ZTg1NDA0YzEyMjNkM2IxZTBjNDBkYTp7Il9hdXRoX3VzZXJfaWQiOiIzNyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiMGUwNjAzNDUwNmEwYjNhMTAyMmYyOGI4NjYwYjU4MzEzZTljMmIxNyJ9', '2022-03-29 16:22:10.544734'),
('y0ve9utm7tupoitj7mm7md0vthkzpvja', 'ZmEyYWE5YjI0ZWQyMzY4OWExMGFhOTk5MGE5MWE5ZTBkY2QxY2JhMjp7Il9hdXRoX3VzZXJfaWQiOiIyOSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzNjNmRlOGE1MTU4NmJhZGMyOGRkMjNhNTc1ZDMwYzRmMDAxMzExNCJ9', '2022-03-17 15:55:57.467222'),
('9b5dvf3bufslbv9l5m1uzb53x9c5t205', 'ZWZhMDgyNDhlYzRjNzFjMjczNjZlMmY2NGFkZmViYjA1NThiZTdkYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlZDhkNDM0NzNiZTkzMzM5NjQzMDBlZTA1ODc4MGJlOWQyNDEyNmU3In0=', '2022-04-04 15:27:06.901349'),
('uynj3dngzdjh0mul353fsmujd6z3c3zy', 'ZWZhMDgyNDhlYzRjNzFjMjczNjZlMmY2NGFkZmViYjA1NThiZTdkYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlZDhkNDM0NzNiZTkzMzM5NjQzMDBlZTA1ODc4MGJlOWQyNDEyNmU3In0=', '2022-05-13 16:12:24.610675'),
('5y9r7hw1e6zhwsbtwisi209yveigjd10', 'ZWZhMDgyNDhlYzRjNzFjMjczNjZlMmY2NGFkZmViYjA1NThiZTdkYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlZDhkNDM0NzNiZTkzMzM5NjQzMDBlZTA1ODc4MGJlOWQyNDEyNmU3In0=', '2022-05-27 16:08:07.698278'),
('9smt9jj9uorijk4jw9aeyxf6nbth9teb', 'ZWZhMDgyNDhlYzRjNzFjMjczNjZlMmY2NGFkZmViYjA1NThiZTdkYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlZDhkNDM0NzNiZTkzMzM5NjQzMDBlZTA1ODc4MGJlOWQyNDEyNmU3In0=', '2023-03-16 17:26:59.898890'),
('pcm9l156d1eocrhii51jyda508ygw3em', 'ZWZhMDgyNDhlYzRjNzFjMjczNjZlMmY2NGFkZmViYjA1NThiZTdkYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlZDhkNDM0NzNiZTkzMzM5NjQzMDBlZTA1ODc4MGJlOWQyNDEyNmU3In0=', '2023-04-17 16:34:41.734953'),
('q0sgymm07dxeq13rwpir9synzu4a3c8o', 'ZWZhMDgyNDhlYzRjNzFjMjczNjZlMmY2NGFkZmViYjA1NThiZTdkYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlZDhkNDM0NzNiZTkzMzM5NjQzMDBlZTA1ODc4MGJlOWQyNDEyNmU3In0=', '2023-05-04 13:56:34.371770'),
('hdb62lhez22lzj251ui4cv4e3zshlee0', 'ODFiYWJmZDJlMjdmYTRmYTYwOWExYzU5NmZiODhlNDc4OTQ0YTBmODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlZDhkNDM0NzNiZTkzMzM5NjQzMDBlZTA1ODc4MGJlOWQyNDEyNmU3IiwiY29uc3VsdGFyX3V0aWxpemFkb3JlcyI6Imh0dHA6Ly8xMC40LjAuOTg6ODU4NS91dGlsaXphZG9yZXMvY29uc3VsdGFydXRpbGl6YWRvcmVzP3BhZ2U9MiJ9', '2023-06-01 16:14:10.763154'),
('p1i1fwomaqpwhmg83aug4n28hay83jw8', 'ZWZhMDgyNDhlYzRjNzFjMjczNjZlMmY2NGFkZmViYjA1NThiZTdkYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlZDhkNDM0NzNiZTkzMzM5NjQzMDBlZTA1ODc4MGJlOWQyNDEyNmU3In0=', '2023-11-01 10:16:56.766680'),
('21wzk5ym52xf2lngjm38m701zxr5sjdv', 'ZWZhMDgyNDhlYzRjNzFjMjczNjZlMmY2NGFkZmViYjA1NThiZTdkYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlZDhkNDM0NzNiZTkzMzM5NjQzMDBlZTA1ODc4MGJlOWQyNDEyNmU3In0=', '2023-11-27 11:52:41.774626'),
('y9mlx4x3p7qewmn6qse1v2abimjoxhu2', 'ZWZhMDgyNDhlYzRjNzFjMjczNjZlMmY2NGFkZmViYjA1NThiZTdkYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlZDhkNDM0NzNiZTkzMzM5NjQzMDBlZTA1ODc4MGJlOWQyNDEyNmU3In0=', '2023-11-27 12:06:43.192626'),
('4sdlv8fx3ya8o2ixamjziwi6m22vx0vs', 'ZWU0MzA4ZTYzNmYyM2FlMWNjYjlmMDFjNzFhOTlhODViMGZlMWMwNjp7Il9hdXRoX3VzZXJfaWQiOiI0MSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQxZDc0MzZmMTJjYjA3MDA2OTM0MGViNmY3NTI3OTYyNTk5ODhkOCJ9', '2024-05-07 23:56:49.404379'),
('px251udmavkunlxsxk07f266drww461n', 'ZWRiNzU0NGEzYTBlZDdkODQ0NzU4YzI0NTcwMmVkYTBhY2Y5MDYwNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwNzY4ODMyMDgxOTExZDg2NmU3NDgyODM1NDcwYmZkMDZjOThjNjQ2Iiwid2l6YXJkX2NyaWFyX2luc2NyaWNhb191bHRpbWFfaG9yYSI6eyJzdGVwIjoiaW5mbyIsInN0ZXBfZGF0YSI6e30sInN0ZXBfZmlsZXMiOnt9LCJleHRyYV9kYXRhIjp7fX19', '2024-06-01 12:30:34.255591');

-- --------------------------------------------------------

--
-- Estrutura da tabela `edificio`
--

CREATE TABLE `edificio` (
  `ID` int(11) NOT NULL,
  `Nome` varchar(64) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `Campus` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `edificio`
--

INSERT INTO `edificio` (`ID`, `Nome`, `image`, `Campus`) VALUES
(4, 'Edifício 8', '', 2),
(5, 'Edificio 2', '', 2),
(6, 'Edifício 7', '', 2),
(3, 'Escola Superior de Educação e Comunicação', '', 1),
(7, 'HORTO', '', 2),
(8, 'Edificio 1', '', 2),
(9, 'Exterior', '', 2),
(10, 'Edifício 1', '', 2),
(11, 'Edifício 4 - CP', '', 2),
(12, 'Artes Visuais', '', 1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `escola`
--

CREATE TABLE `escola` (
  `id` int(11) NOT NULL,
  `nome` varchar(200) NOT NULL,
  `local` varchar(128) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `escola`
--

INSERT INTO `escola` (`id`, `nome`, `local`) VALUES
(1, 'ww', 'Faro'),
(2, '33', 'Faro'),
(3, 'teste', 'Faro'),
(4, 'Faro', 'Faro');

-- --------------------------------------------------------

--
-- Estrutura da tabela `espaco`
--

CREATE TABLE `espaco` (
  `ID` int(11) NOT NULL,
  `Nome` varchar(255) NOT NULL,
  `Andar` varchar(255) NOT NULL,
  `Descricao` varchar(255) DEFAULT NULL,
  `Edificio` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `espaco`
--

INSERT INTO `espaco` (`ID`, `Nome`, `Andar`, `Descricao`, `Edificio`) VALUES
(29, 'Hall de entrada', '1', 'Entrada', 4),
(6, 'Sala 31', '0', NULL, 3),
(30, 'Hall de entrada', '0', 'Perto da estátua em frente da escadaria. Em frente da biblioteca', 5),
(7, 'Sala 40', '', NULL, 3),
(8, 'Corredor da sala', '', NULL, 3),
(9, 'Hall da sala 40', '', NULL, 3),
(10, 'Sala 41', '', NULL, 3),
(11, 'Sala 62', '', NULL, 3),
(12, 'Sala 63', '', NULL, 3),
(13, 'Sala 63A', '', NULL, 3),
(14, 'Sala 95', '', NULL, 3),
(15, 'Sala 96', '', NULL, 3),
(16, 'Sala 97', '', NULL, 3),
(17, 'Sala 98', '', NULL, 3),
(18, 'Sala 99', '', NULL, 3),
(19, 'Átrio (98/99)', '', NULL, 3),
(20, 'Sala 105', '', NULL, 3),
(21, 'Sala UP', '', NULL, 3),
(22, 'Átrio 1.º andar', '', NULL, 3),
(23, 'Corredor 1º and', '', NULL, 3),
(24, 'Lab. C. Desporto', '', 'Laboratório de Ciências do Desporto', 3),
(25, 'Ginásio', '', NULL, 3),
(26, 'Espaço Mostra', '', NULL, 3),
(27, 'Auditório', '', 'Auditório Paulo Freire', 3),
(28, 'Sala 22', '', NULL, 3),
(31, 'Hall de entrada norte', '1', 'Entrada', 6),
(32, 'Entrada', '0', 'Entrada', 7),
(33, '1.53', '1', 'Sala de Informática', 8),
(34, 'Exterior do Edificio 7', '1', 'Junto à entrada norte', 9),
(35, 'Sala 0.20', '-1', NULL, 10),
(36, 'Sala 0.21', '', NULL, 10),
(37, 'Sala 0.22', '', NULL, 10),
(38, 'Sala 0.23', '', NULL, 10),
(39, 'Sala 0.35', '', NULL, 10),
(40, 'Sala 1.1', '', NULL, 10),
(41, 'Sala 1.2', '', NULL, 10),
(42, 'Sala 1.36', '', NULL, 10),
(43, 'Sala 1.37', '', NULL, 10),
(44, 'Sala 1.56', '', NULL, 10),
(45, 'Sala 1.6', '', NULL, 10),
(46, 'Sala 1.7', '', NULL, 10),
(47, 'Sala 1.8', '', NULL, 10),
(48, 'Sala 2.1', '', NULL, 10),
(49, 'Sala 2.2', '', NULL, 10),
(50, 'Sala 2.37', '', NULL, 10),
(51, 'Sala 2.4', '', NULL, 10),
(52, 'Sala 2.5', '', NULL, 10),
(53, 'Sala 2.6', '', NULL, 10),
(54, 'Sala 2.7', '', NULL, 10),
(55, 'Sala 2.8', '', NULL, 10),
(56, 'Lab. Arqueologia', '', NULL, 10),
(57, 'Sala de Espelhos', '', NULL, 10),
(58, 'Anfiteatro A', '1', NULL, 11),
(59, 'Anfiteatro B', '', NULL, 11),
(60, 'Anfiteatro C', '', NULL, 11),
(61, 'Anfiteatro D', '', NULL, 11),
(62, 'Anfiteatro E', '', NULL, 11),
(63, 'Anfiteatro F', '', NULL, 11),
(64, 'Edifício das Oficinas (ST)', '0', NULL, 12),
(65, 'Sala 1.4', '', NULL, 12);

-- --------------------------------------------------------

--
-- Estrutura da tabela `estado`
--

CREATE TABLE `estado` (
  `id` int(11) NOT NULL,
  `estado` varchar(10) NOT NULL,
  `questionario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `estado`
--

INSERT INTO `estado` (`id`, `estado`, `questionario_id`) VALUES
(1, 'criado', 2),
(2, 'criado', 1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `horario`
--

CREATE TABLE `horario` (
  `ID` int(11) NOT NULL,
  `Inicio` time(6) NOT NULL,
  `Fim` time(6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `horario`
--

INSERT INTO `horario` (`ID`, `Inicio`, `Fim`) VALUES
(1, '12:00:00.000000', '14:00:00.000000'),
(2, '09:30:00.000000', '09:50:00.000000'),
(3, '10:30:00.000000', '10:50:00.000000'),
(4, '11:30:00.000000', '11:50:00.000000'),
(5, '14:30:00.000000', '14:50:00.000000'),
(6, '16:30:00.000000', '16:50:00.000000'),
(7, '09:00:00.000000', '09:05:00.000000'),
(8, '15:00:00.000000', '15:05:00.000000'),
(9, '09:10:00.000000', '09:15:00.000000'),
(10, '09:20:00.000000', '09:25:00.000000'),
(11, '09:30:00.000000', '09:35:00.000000'),
(12, '10:00:00.000000', '10:05:00.000000'),
(13, '11:00:00.000000', '11:05:00.000000'),
(14, '10:00:00.000000', '11:00:00.000000'),
(15, '14:00:00.000000', '14:05:00.000000'),
(16, '14:00:00.000000', '15:00:00.000000'),
(17, '14:00:00.000000', '20:00:00.000000'),
(18, '10:00:00.000000', '16:00:00.000000'),
(19, '10:00:00.000000', '13:00:00.000000'),
(20, '14:30:00.000000', '17:30:00.000000'),
(21, '10:00:00.000000', '12:30:00.000000'),
(22, '14:30:00.000000', '17:00:00.000000'),
(23, '10:00:00.000000', '12:00:00.000000'),
(24, '14:30:00.000000', '16:00:00.000000'),
(25, '17:30:00.000000', '18:00:00.000000'),
(26, '15:30:00.000000', '16:00:00.000000'),
(27, '11:00:00.000000', '13:30:00.000000'),
(28, '14:30:00.000000', '15:00:00.000000'),
(29, '14:30:00.000000', '15:30:00.000000'),
(30, '09:00:00.000000', '17:00:00.000000'),
(31, '02:07:00.000000', '03:01:00.000000'),
(32, '02:10:00.000000', '03:10:00.000000'),
(33, '10:00:00.000000', '16:00:00.000000'),
(34, '09:00:00.000000', '17:00:00.000000'),
(35, '09:30:00.000000', '16:15:00.000000'),
(36, '11:52:00.000000', '17:00:00.000000'),
(37, '11:52:00.000000', '17:00:00.000000'),
(38, '11:52:00.000000', '17:00:00.000000'),
(39, '11:52:00.000000', '17:00:00.000000'),
(40, '11:52:00.000000', '17:00:00.000000'),
(41, '14:05:00.000000', '14:06:00.000000'),
(42, '14:05:00.000000', '14:06:00.000000'),
(43, '14:08:00.000000', '15:10:00.000000'),
(44, '10:23:00.000000', '16:19:00.000000'),
(45, '14:55:00.000000', '15:55:00.000000'),
(46, '14:55:00.000000', '15:55:00.000000'),
(47, '14:00:00.000000', '15:55:00.000000'),
(48, '13:00:00.000000', '15:55:00.000000'),
(49, '09:30:00.000000', '15:50:00.000000'),
(50, '09:00:00.000000', '14:00:00.000000'),
(51, '13:01:00.000000', '15:02:00.000000'),
(52, '10:33:00.000000', '16:28:00.000000'),
(53, '11:47:00.000000', '17:00:00.000000'),
(54, '12:45:00.000000', '16:44:00.000000'),
(55, '08:59:00.000000', '16:53:00.000000'),
(56, '11:00:00.000000', '16:53:00.000000'),
(57, '12:27:00.000000', '16:53:00.000000'),
(58, '13:30:00.000000', '15:26:00.000000'),
(59, '14:00:00.000000', '16:53:00.000000'),
(60, '13:02:00.000000', '16:53:00.000000'),
(61, '11:00:00.000000', '14:00:00.000000');

-- --------------------------------------------------------

--
-- Estrutura da tabela `idioma`
--

CREATE TABLE `idioma` (
  `ID` int(11) NOT NULL,
  `Nome` varchar(255) DEFAULT NULL,
  `Sigla` varchar(255) DEFAULT NULL,
  `DiaAbertoID` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `informacaomensagem`
--

CREATE TABLE `informacaomensagem` (
  `id` int(11) NOT NULL,
  `data` datetime(6) NOT NULL,
  `pendente` tinyint(1) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descricao` varchar(255) NOT NULL,
  `tipo` varchar(255) NOT NULL,
  `lido` tinyint(1) NOT NULL,
  `emissorid` int(11) DEFAULT NULL,
  `recetorid` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `informacaomensagem`
--

INSERT INTO `informacaomensagem` (`id`, `data`, `pendente`, `titulo`, `descricao`, `tipo`, `lido`, `emissorid`, `recetorid`) VALUES
(15, '2023-04-20 14:24:19.421295', 1, 'aa', 'aa', 'Grupo de administradores do dia aberto', 0, 1, 23),
(13, '2023-04-20 14:22:07.304034', 1, 'fe', 'fdefdef', 'Grupo de administradores do dia aberto', 0, 1, 23),
(14, '2023-04-20 14:24:19.405685', 1, 'aa', 'aa', 'Grupo de administradores do dia aberto', 0, 1, 1),
(12, '2023-04-20 14:22:07.225906', 1, 'fe', 'fdefdef', 'Grupo de administradores do dia aberto', 0, 1, 1),
(11, '2022-04-29 14:51:21.897893', 0, 'ver email', 'dia aberto', 'Individual', 1, 1, 26);

-- --------------------------------------------------------

--
-- Estrutura da tabela `informacaonotificacao`
--

CREATE TABLE `informacaonotificacao` (
  `id` int(11) NOT NULL,
  `data` datetime(6) NOT NULL,
  `pendente` tinyint(1) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descricao` varchar(255) NOT NULL,
  `tipo` varchar(255) NOT NULL,
  `lido` tinyint(1) NOT NULL,
  `emissorid` int(11) DEFAULT NULL,
  `recetorid` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `informacaonotificacao`
--

INSERT INTO `informacaonotificacao` (`id`, `data`, `pendente`, `titulo`, `descricao`, `tipo`, `lido`, `emissorid`, `recetorid`) VALUES
(46, '2022-03-03 10:23:20.762274', 1, 'Validação de registos de utilizadores pendentes', 'Foram feitos registos de utilizadores na plataforma que necessitam de ser validados.', 'register 28', 0, 28, 28),
(82, '2022-03-20 16:12:53.977966', 1, 'Validação de registos de utilizadores pendentes', 'Foram feitos registos de utilizadores na plataforma que necessitam de ser validados.', 'register 37', 0, 37, 36),
(79, '2022-03-20 16:03:55.139438', 1, 'Validação de registos de utilizadores pendentes', 'Foram feitos registos de utilizadores na plataforma que necessitam de ser validados.', 'register 36', 0, 36, 36),
(62, '2022-03-07 16:10:57.568869', 1, 'Validação de registos de utilizadores pendentes', 'Foram feitos registos de utilizadores na plataforma que necessitam de ser validados.', 'register 32', 0, 32, 32),
(83, '2022-03-20 18:29:03.772965', 1, 'Existem atividades por validar', 'Foram criadas propostas de atividades que têm de ser validadas.', 'atividade 21', 0, 37, 36),
(87, '2023-05-23 16:13:25.671367', 1, 'Validação de registos de utilizadores pendentes', 'Foram feitos registos de utilizadores na plataforma que necessitam de ser validados.', 'register 39', 0, 39, 31),
(74, '2022-03-12 12:12:17.096803', 1, 'Validação de registos de utilizadores pendentes', 'Foram feitos registos de utilizadores na plataforma que necessitam de ser validados.', 'register 34', 0, 34, 34),
(86, '2023-05-23 16:13:25.640111', 1, 'Validação de registos de utilizadores pendentes', 'Foram feitos registos de utilizadores na plataforma que necessitam de ser validados.', 'register 39', 0, 39, 23),
(89, '2024-04-28 16:42:11.868052', 1, 'Validação de registos de utilizadores pendentes', 'Foram feitos registos de utilizadores na plataforma que necessitam de ser validados.', 'register 41', 0, 41, 23),
(90, '2024-04-28 16:42:11.890696', 1, 'Validação de registos de utilizadores pendentes', 'Foram feitos registos de utilizadores na plataforma que necessitam de ser validados.', 'register 41', 0, 41, 31);

-- --------------------------------------------------------

--
-- Estrutura da tabela `inscricao`
--

CREATE TABLE `inscricao` (
  `id` int(11) NOT NULL,
  `individual` tinyint(1) NOT NULL,
  `nalunos` int(11) NOT NULL,
  `ano` int(11) DEFAULT NULL,
  `turma` varchar(1) DEFAULT NULL,
  `areacientifica` varchar(64) DEFAULT NULL,
  `dia` date NOT NULL,
  `meio_transporte` varchar(40) NOT NULL,
  `hora_chegada` time(6) DEFAULT NULL,
  `local_chegada` varchar(200) DEFAULT NULL,
  `entrecampi` tinyint(1) NOT NULL,
  `diaaberto_id` int(11) NOT NULL,
  `escola_id` int(11) NOT NULL,
  `participante_id` int(11) NOT NULL,
  `nr_presentes` int(11) NOT NULL,
  `presenca` tinyint(1) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `inscricao`
--

INSERT INTO `inscricao` (`id`, `individual`, `nalunos`, `ano`, `turma`, `areacientifica`, `dia`, `meio_transporte`, `hora_chegada`, `local_chegada`, `entrecampi`, `diaaberto_id`, `escola_id`, `participante_id`, `nr_presentes`, `presenca`) VALUES
(4, 0, 18, 11, 'h', 'geral', '2022-05-03', 'comboio', '10:00:00.000000', 'Estação de Comboios de Faro', 1, 3, 4, 33, 0, 0),
(3, 0, 30, 9, 'g', 'geral', '2022-05-03', 'comboio', '09:00:00.000000', 'Terminal', 1, 3, 3, 33, 0, 0);

-- --------------------------------------------------------

--
-- Estrutura da tabela `inscricaoprato`
--

CREATE TABLE `inscricaoprato` (
  `id` int(11) NOT NULL,
  `npratosalunos` int(11) NOT NULL,
  `npratosdocentes` int(11) NOT NULL,
  `campus_id` int(11) NOT NULL,
  `inscricao_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `inscricaoprato`
--

INSERT INTO `inscricaoprato` (`id`, `npratosalunos`, `npratosdocentes`, `campus_id`, `inscricao_id`) VALUES
(1, 6, 1, 1, 3),
(2, 4, 1, 2, 4);

-- --------------------------------------------------------

--
-- Estrutura da tabela `inscricaosessao`
--

CREATE TABLE `inscricaosessao` (
  `id` int(11) NOT NULL,
  `nparticipantes` int(11) NOT NULL,
  `inscricao_id` int(11) NOT NULL,
  `sessao_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `inscricaosessao`
--

INSERT INTO `inscricaosessao` (`id`, `nparticipantes`, `inscricao_id`, `sessao_id`) VALUES
(6, 1, 4, 34),
(5, 4, 3, 32),
(4, 4, 3, 19);

-- --------------------------------------------------------

--
-- Estrutura da tabela `inscricaotransporte`
--

CREATE TABLE `inscricaotransporte` (
  `id` int(11) NOT NULL,
  `npassageiros` int(11) NOT NULL,
  `inscricao_id` int(11) NOT NULL,
  `transporte_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `inscricaotransporte`
--

INSERT INTO `inscricaotransporte` (`id`, `npassageiros`, `inscricao_id`, `transporte_id`) VALUES
(1, 30, 3, 10),
(2, 30, 3, 24);

-- --------------------------------------------------------

--
-- Estrutura da tabela `materiais`
--

CREATE TABLE `materiais` (
  `ID` int(11) NOT NULL,
  `nome` varchar(255) DEFAULT NULL,
  `AtividadeID` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `materiais`
--

INSERT INTO `materiais` (`ID`, `nome`, `AtividadeID`) VALUES
(8, NULL, 8),
(7, NULL, 7),
(10, 'Projetor, 16 telemóveis', 10),
(11, 'Projetores', 11),
(12, 'Projetores', 12),
(13, NULL, 13),
(14, NULL, 14),
(15, NULL, 15),
(16, NULL, 16),
(17, NULL, 17),
(18, NULL, 18),
(19, NULL, 19),
(21, NULL, 21),
(22, NULL, 22),
(23, NULL, 23),
(24, NULL, 24),
(25, NULL, 25),
(26, NULL, 26),
(27, NULL, 27),
(28, NULL, 28),
(29, NULL, 29),
(30, NULL, 30),
(31, NULL, 31);

-- --------------------------------------------------------

--
-- Estrutura da tabela `mensagemenviada`
--

CREATE TABLE `mensagemenviada` (
  `id` int(11) NOT NULL,
  `mensagem_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `mensagemenviada`
--

INSERT INTO `mensagemenviada` (`id`, `mensagem_id`) VALUES
(7, 15),
(6, 13),
(5, 11);

-- --------------------------------------------------------

--
-- Estrutura da tabela `mensagemrecebida`
--

CREATE TABLE `mensagemrecebida` (
  `id` int(11) NOT NULL,
  `mensagem_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `mensagemrecebida`
--

INSERT INTO `mensagemrecebida` (`id`, `mensagem_id`) VALUES
(13, 15),
(12, 13),
(11, 11);

-- --------------------------------------------------------

--
-- Estrutura da tabela `menu`
--

CREATE TABLE `menu` (
  `ID` int(11) NOT NULL,
  `Dia` date NOT NULL,
  `Campus` int(11) NOT NULL,
  `diaAberto` int(11) NOT NULL,
  `HorarioID` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `menu`
--

INSERT INTO `menu` (`ID`, `Dia`, `Campus`, `diaAberto`, `HorarioID`) VALUES
(1, '2022-05-03', 1, 3, 1),
(2, '2022-05-04', 1, 3, 1),
(3, '2022-05-03', 2, 3, 1),
(4, '2022-05-04', 2, 3, 1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `notificacao`
--

CREATE TABLE `notificacao` (
  `id` int(11) NOT NULL,
  `level` varchar(20) NOT NULL,
  `unread` tinyint(1) NOT NULL,
  `actor_object_id` varchar(255) NOT NULL,
  `verb` varchar(255) NOT NULL,
  `description` longtext DEFAULT NULL,
  `target_object_id` varchar(255) DEFAULT NULL,
  `action_object_object_id` varchar(255) DEFAULT NULL,
  `timestamp` datetime(6) NOT NULL,
  `public` tinyint(1) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `emailed` tinyint(1) NOT NULL,
  `data` longtext DEFAULT NULL,
  `titulo` varchar(255) NOT NULL,
  `descricao` varchar(255) NOT NULL,
  `tipo` varchar(255) NOT NULL,
  `action_object_content_type_id` int(11) DEFAULT NULL,
  `actor_content_type_id` int(11) NOT NULL,
  `recipient_id` int(11) NOT NULL,
  `target_content_type_id` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `notificacao`
--

INSERT INTO `notificacao` (`id`, `level`, `unread`, `actor_object_id`, `verb`, `description`, `target_object_id`, `action_object_object_id`, `timestamp`, `public`, `deleted`, `emailed`, `data`, `titulo`, `descricao`, `tipo`, `action_object_content_type_id`, `actor_content_type_id`, `recipient_id`, `target_content_type_id`) VALUES
(24, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"Recursos Naturais e Biotecnologia\"', 'Foi alterada uma atividade', '7', NULL, '2022-03-03 11:17:40.339523', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(23, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"Recursos Naturais e Biotecnologia\"', 'Foi alterada uma atividade', '7', NULL, '2022-03-03 11:17:26.150974', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(21, 'warning', 1, '26', 'Foi feita uma alteração na atividade \"Desafios nos Laboratórios de Química e Ciências Farmacêuticas\"', 'Foi alterada uma atividade', '8', NULL, '2022-03-01 23:04:53.438530', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(22, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"Recursos Naturais e Biotecnologia\"', 'Foi alterada uma atividade', '7', NULL, '2022-03-03 11:12:29.854447', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(18, 'warning', 1, '26', 'Foi feita uma alteração na atividade \"Desafios nos Laboratórios de Química e Ciências Farmacêuticas\"', 'Foi alterada uma atividade', '8', NULL, '2022-02-28 15:57:55.004061', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(19, 'warning', 1, '26', 'Foi feita uma alteração na atividade \"Desafios nos Laboratórios de Química e Ciências Farmacêuticas\"', 'Foi alterada uma atividade', '8', NULL, '2022-02-28 16:36:59.327451', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(20, 'warning', 1, '26', 'Foi feita uma alteração na atividade \"Desafios nos Laboratórios de Química e Ciências Farmacêuticas\"', 'Foi alterada uma atividade', '8', NULL, '2022-03-01 22:55:56.018713', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(25, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"As 20 000 léguas subterrâneas\"', 'Foi alterada uma atividade', '15', NULL, '2022-03-03 11:28:55.054810', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(26, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"Recursos Naturais e Biotecnologia\"', 'Foi alterada uma atividade', '7', NULL, '2022-03-03 11:29:13.676012', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(27, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"Recursos Naturais e Biotecnologia\"', 'Foi alterada uma atividade', '7', NULL, '2022-03-03 11:29:50.905650', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(28, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"Recursos Naturais e Biotecnologia\"', 'Foi alterada uma atividade', '7', NULL, '2022-03-03 11:44:39.808962', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(29, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"Ciências do Mar: organismos, ambientes e investigadores\"', 'Foi alterada uma atividade', '17', NULL, '2022-03-03 11:44:54.803485', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(30, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"Recursos Naturais e Biotecnologia\"', 'Foi alterada uma atividade', '7', NULL, '2022-03-03 11:57:02.822864', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(31, 'success', 0, '31', 'A sua proposta de atividade \"Tecnologia na nossa vida\" foi aceite.', 'Confirmação da atividade proposta', '10', NULL, '2022-03-03 12:02:03.306142', 0, 0, 0, NULL, '', '', '', NULL, 3, 26, 7),
(32, 'success', 0, '31', 'A sua proposta de atividade \"Matemática para sempre\" foi aceite.', 'Confirmação da atividade proposta', '11', NULL, '2022-03-03 12:02:11.137080', 0, 0, 0, NULL, '', '', '', NULL, 3, 26, 7),
(33, 'success', 0, '31', 'A sua proposta de atividade \"Física e Matemática, ontem e hoje\" foi aceite.', 'Confirmação da atividade proposta', '12', NULL, '2022-03-03 12:02:16.881882', 0, 0, 0, NULL, '', '', '', NULL, 3, 26, 7),
(34, 'success', 0, '31', 'A sua proposta de atividade \"Desafios nos Laboratórios de Química e Ciências Farmacêuticas\" foi aceite.', 'Confirmação da atividade proposta', '8', NULL, '2022-03-03 12:02:27.096099', 0, 0, 0, NULL, '', '', '', NULL, 3, 26, 7),
(35, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"Da célula aos implantes artificiais: ciências e tecnologias\"', 'Foi alterada uma atividade', '19', NULL, '2022-03-03 12:07:23.638074', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(36, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"Fases do ciclo de vida de animais marinhos\"', 'Foi alterada uma atividade', '18', NULL, '2022-03-03 12:07:47.566053', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(37, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"Ciências do Mar: organismos, ambientes e investigadores\"', 'Foi alterada uma atividade', '17', NULL, '2022-03-03 12:08:18.091626', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(38, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"Métodos em Ciências do Mar\"', 'Foi alterada uma atividade', '16', NULL, '2022-03-03 12:08:38.004596', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(39, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"As 20 000 léguas subterrâneas\"', 'Foi alterada uma atividade', '15', NULL, '2022-03-03 12:09:10.083593', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(40, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"O cultivo das plantas: the sky is the limit!\"', 'Foi alterada uma atividade', '14', NULL, '2022-03-03 12:09:36.818104', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(41, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"SOS URBAN: espaços verdes sustentáveis\"', 'Foi alterada uma atividade', '13', NULL, '2022-03-03 12:10:04.309304', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(42, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"Recursos Naturais e Biotecnologia\"', 'Foi alterada uma atividade', '7', NULL, '2022-03-03 12:10:30.972505', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(43, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"Ciências do Mar: organismos, ambientes e investigadores\"', 'Foi alterada uma atividade', '17', NULL, '2022-03-03 12:10:48.698634', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(44, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"Recursos Naturais e Biotecnologia\"', 'Foi alterada uma atividade', '7', NULL, '2022-03-03 12:11:37.934701', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(45, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"SOS URBAN: espaços verdes sustentáveis\"', 'Foi alterada uma atividade', '13', NULL, '2022-03-03 12:12:07.782495', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(46, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"O cultivo das plantas: the sky is the limit!\"', 'Foi alterada uma atividade', '14', NULL, '2022-03-03 12:12:32.739852', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(47, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"Métodos em Ciências do Mar\"', 'Foi alterada uma atividade', '16', NULL, '2022-03-03 12:13:05.269911', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(48, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"Recursos Naturais e Biotecnologia\"', 'Foi alterada uma atividade', '7', NULL, '2022-03-03 12:13:25.050100', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(49, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"O cultivo das plantas: the sky is the limit!\"', 'Foi alterada uma atividade', '14', NULL, '2022-03-03 12:13:49.795646', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(50, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"Métodos em Ciências do Mar\"', 'Foi alterada uma atividade', '16', NULL, '2022-03-03 12:14:03.077212', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(51, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"Ciências do Mar: organismos, ambientes e investigadores\"', 'Foi alterada uma atividade', '17', NULL, '2022-03-03 12:14:27.896320', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(52, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"Fases do ciclo de vida de animais marinhos\"', 'Foi alterada uma atividade', '18', NULL, '2022-03-03 12:14:43.247827', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(53, 'warning', 1, '25', 'Foi feita uma alteração na atividade \"Da célula aos implantes artificiais: ciências e tecnologias\"', 'Foi alterada uma atividade', '19', NULL, '2022-03-03 12:14:57.522582', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(54, 'success', 1, '31', 'A sua proposta de atividade \"Da célula aos implantes artificiais: ciências e tecnologias\" foi aceite.', 'Confirmação da atividade proposta', '19', NULL, '2022-03-03 12:18:12.782010', 0, 0, 0, NULL, '', '', '', NULL, 3, 25, 7),
(55, 'success', 1, '31', 'A sua proposta de atividade \"Fases do ciclo de vida de animais marinhos\" foi aceite.', 'Confirmação da atividade proposta', '18', NULL, '2022-03-03 12:18:19.172414', 0, 0, 0, NULL, '', '', '', NULL, 3, 25, 7),
(56, 'success', 1, '31', 'A sua proposta de atividade \"Ciências do Mar: organismos, ambientes e investigadores\" foi aceite.', 'Confirmação da atividade proposta', '17', NULL, '2022-03-03 12:18:26.961240', 0, 0, 0, NULL, '', '', '', NULL, 3, 25, 7),
(57, 'success', 1, '31', 'A sua proposta de atividade \"Métodos em Ciências do Mar\" foi aceite.', 'Confirmação da atividade proposta', '16', NULL, '2022-03-03 12:18:32.858560', 0, 0, 0, NULL, '', '', '', NULL, 3, 25, 7),
(58, 'success', 1, '31', 'A sua proposta de atividade \"As 20 000 léguas subterrâneas\" foi aceite.', 'Confirmação da atividade proposta', '15', NULL, '2022-03-03 12:18:40.041332', 0, 0, 0, NULL, '', '', '', NULL, 3, 25, 7),
(59, 'success', 1, '31', 'A sua proposta de atividade \"O cultivo das plantas: the sky is the limit!\" foi aceite.', 'Confirmação da atividade proposta', '14', NULL, '2022-03-03 12:18:49.915707', 0, 0, 0, NULL, '', '', '', NULL, 3, 25, 7),
(60, 'success', 1, '31', 'A sua proposta de atividade \"SOS URBAN: espaços verdes sustentáveis\" foi aceite.', 'Confirmação da atividade proposta', '13', NULL, '2022-03-03 12:18:57.127518', 0, 0, 0, NULL, '', '', '', NULL, 3, 25, 7),
(61, 'success', 1, '31', 'A sua proposta de atividade \"Recursos Naturais e Biotecnologia\" foi aceite.', 'Confirmação da atividade proposta', '7', NULL, '2022-03-03 12:19:50.159759', 0, 0, 0, NULL, '', '', '', NULL, 3, 25, 7),
(62, 'warning', 1, '26', 'Foi feita uma alteração na atividade \"Matemática para sempre\"', 'Foi alterada uma atividade', '11', NULL, '2022-03-10 18:52:37.829934', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(63, 'warning', 1, '26', 'Foi feita uma alteração na atividade \"Física e Matemática, ontem e hoje\"', 'Foi alterada uma atividade', '12', NULL, '2022-03-10 18:55:15.674924', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(64, 'success', 0, '31', 'A sua proposta de atividade \"Física e Matemática, ontem e hoje\" foi aceite.', 'Confirmação da atividade proposta', '12', NULL, '2022-03-10 18:55:55.243019', 0, 0, 0, NULL, '', '', '', NULL, 3, 26, 7),
(65, 'success', 0, '31', 'A sua proposta de atividade \"Matemática para sempre\" foi aceite.', 'Confirmação da atividade proposta', '11', NULL, '2022-03-10 18:56:02.216542', 0, 0, 0, NULL, '', '', '', NULL, 3, 26, 7),
(66, 'success', 0, '31', 'A sua proposta de atividade \"Física e Matemática, ontem e hoje\" foi aceite.', 'Confirmação da atividade proposta', '12', NULL, '2022-03-15 15:54:42.573222', 0, 0, 0, NULL, '', '', '', NULL, 3, 26, 7),
(67, 'warning', 1, '26', 'Foi feita uma alteração na atividade \"Física e Matemática, ontem e hoje\"', 'Foi alterada uma atividade', '12', NULL, '2022-03-15 16:15:16.534485', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(68, 'success', 0, '31', 'A sua proposta de atividade \"Física e Matemática, ontem e hoje\" foi aceite.', 'Confirmação da atividade proposta', '12', NULL, '2022-03-15 16:16:44.564607', 0, 0, 0, NULL, '', '', '', NULL, 3, 26, 7),
(69, 'warning', 1, '26', 'Foi feita uma alteração na atividade \"Física e Matemática, ontem e hoje\"', 'Foi alterada uma atividade', '12', NULL, '2023-04-19 09:19:06.230056', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(70, 'warning', 1, '26', 'Foi feita uma alteração na atividade \"Tecnologia na nossa vida\"', 'Foi alterada uma atividade', '10', NULL, '2023-04-19 09:20:51.437348', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(71, 'success', 1, '31', 'A sua proposta de atividade \"Física e Matemática, ontem e hoje\" foi aceite.', 'Confirmação da atividade proposta', '12', NULL, '2023-04-19 09:21:19.078054', 0, 0, 0, NULL, '', '', '', NULL, 3, 26, 7),
(72, 'success', 1, '31', 'A sua proposta de atividade \"Tecnologia na nossa vida\" foi aceite.', 'Confirmação da atividade proposta', '10', NULL, '2023-04-19 09:21:27.867533', 0, 0, 0, NULL, '', '', '', NULL, 3, 26, 7),
(73, 'error', 1, '31', 'A sua proposta de atividade Teste foi rejeitada.', 'Rejeição da atividade proposta', '22', NULL, '2023-04-19 09:32:41.044468', 0, 0, 0, NULL, '', '', '', NULL, 3, 26, 7),
(74, 'warning', 1, '26', 'Foi feita uma alteração na atividade \"Tecnologia na nossa vida\"', 'Foi alterada uma atividade', '10', NULL, '2023-04-19 09:33:50.083782', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(75, 'warning', 1, '26', 'Foi feita uma alteração na atividade \"Teste\"', 'Foi alterada uma atividade', '22', NULL, '2023-04-19 09:34:00.825063', 0, 0, 0, NULL, '', '', '', NULL, 3, 31, 7),
(76, 'success', 1, '31', 'A sua proposta de atividade \"Teste\" foi aceite.', 'Confirmação da atividade proposta', '22', NULL, '2023-04-19 09:34:20.952367', 0, 0, 0, NULL, '', '', '', NULL, 3, 26, 7),
(77, 'success', 1, '31', 'A sua proposta de atividade \"Tecnologia na nossa vida\" foi aceite.', 'Confirmação da atividade proposta', '10', NULL, '2023-04-19 09:34:31.772402', 0, 0, 0, NULL, '', '', '', NULL, 3, 26, 7);

-- --------------------------------------------------------

--
-- Estrutura da tabela `opcaoresposta`
--

CREATE TABLE `opcaoresposta` (
  `id` int(11) NOT NULL,
  `texto` varchar(200) NOT NULL,
  `pergunta_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `participante`
--

CREATE TABLE `participante` (
  `utilizador_ptr_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `participante`
--

INSERT INTO `participante` (`utilizador_ptr_id`) VALUES
(33),
(38),
(40);

-- --------------------------------------------------------

--
-- Estrutura da tabela `pergunta`
--

CREATE TABLE `pergunta` (
  `id` int(11) NOT NULL,
  `texto` varchar(300) NOT NULL,
  `tipo` varchar(30) NOT NULL,
  `questionario_id` int(11) NOT NULL,
  `tema_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `pergunta`
--

INSERT INTO `pergunta` (`id`, `texto`, `tipo`, `questionario_id`, `tema_id`) VALUES
(1, 'asds', 'porExtenso', 1, 1),
(2, 'asds', 'porExtenso', 2, 1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `prato`
--

CREATE TABLE `prato` (
  `ID` int(11) NOT NULL,
  `Prato` varchar(255) NOT NULL,
  `Tipo` varchar(255) NOT NULL,
  `NrPratosDisponiveis` int(11) NOT NULL,
  `MenuID` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `prato`
--

INSERT INTO `prato` (`ID`, `Prato`, `Tipo`, `NrPratosDisponiveis`, `MenuID`) VALUES
(1, 'Refeição completa (prato de carne)', 'Carne', 1000, 1),
(2, 'Refeição completa (prato de peixe)', 'Peixe', 1000, 1),
(3, 'Refeição completa (vegetariana)', 'Vegetariano', 1000, 1),
(4, 'Refeição completa (prato de carne)', 'Carne', 1000, 2),
(5, 'Refeição completa (prato de peixe)', 'Peixe', 1000, 2),
(6, 'Refeição completa (vegetariana)', 'Vegetariano', 1000, 2),
(7, 'Refeição completa (prato de carne)', 'Carne', 1000, 3),
(8, 'Refeição completa (prato de peixe)', 'Peixe', 1000, 3),
(9, 'Refeição completa (vegetariana)', 'Vegetariano', 1000, 3),
(10, 'Refeição completa (prato de carne)', 'Carne', 1000, 4),
(11, 'Refeição completa (prato de peixe)', 'Peixe', 1000, 4),
(12, 'Refeição completa (vegetariana)', 'Vegetariano', 1000, 4);

-- --------------------------------------------------------

--
-- Estrutura da tabela `preferencia`
--

CREATE TABLE `preferencia` (
  `ID` int(11) NOT NULL,
  `Tipo` varchar(64) NOT NULL,
  `ColaboradorUtilizadorID` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `preferenciaatividade`
--

CREATE TABLE `preferenciaatividade` (
  `ID` int(11) NOT NULL,
  `Atividade` int(11) DEFAULT NULL,
  `PreferenciaID` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `professoruniversitario`
--

CREATE TABLE `professoruniversitario` (
  `utilizador_ptr_id` int(11) NOT NULL,
  `Gabinete` varchar(255) NOT NULL,
  `departamento_id` int(11) NOT NULL,
  `faculdade_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `professoruniversitario`
--

INSERT INTO `professoruniversitario` (`utilizador_ptr_id`, `Gabinete`, `departamento_id`, `faculdade_id`) VALUES
(26, '2.69', 21, 6),
(25, '3.8', 21, 6),
(35, '1.32', 20, 5),
(37, 'Sala 1.46', 11, 5),
(39, '2.69', 14, 6);

-- --------------------------------------------------------

--
-- Estrutura da tabela `questionario`
--

CREATE TABLE `questionario` (
  `id` int(11) NOT NULL,
  `titulo` varchar(200) NOT NULL,
  `descricao` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `data_publicacao` datetime(6) DEFAULT NULL,
  `diaaberto_id` int(11) NOT NULL,
  `data_arquivo` datetime(6) DEFAULT NULL,
  `data_validacao` datetime(6) DEFAULT NULL,
  `estado_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `questionario`
--

INSERT INTO `questionario` (`id`, `titulo`, `descricao`, `created_at`, `data_publicacao`, `diaaberto_id`, `data_arquivo`, `data_validacao`, `estado_id`) VALUES
(1, 'TESTE', 'OLA', '2024-04-23 23:36:40.552372', NULL, 6, '2024-05-18 12:56:13.557727', NULL, 2),
(2, 'TESTE1', 'POD', '2024-05-18 12:49:59.004060', NULL, 6, NULL, NULL, 1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `responsavel`
--

CREATE TABLE `responsavel` (
  `id` int(11) NOT NULL,
  `nome` varchar(128) NOT NULL,
  `email` varchar(128) NOT NULL,
  `tel` varchar(128) NOT NULL,
  `inscricao_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `responsavel`
--

INSERT INTO `responsavel` (`id`, `nome`, `email`, `tel`, `inscricao_id`) VALUES
(4, 'Ivete Silva', 'info@ualg.pt', '+351963107359', 4),
(3, 'Ivete Silva', 'info@ualg.pt', '+351963107359', 3);

-- --------------------------------------------------------

--
-- Estrutura da tabela `resposta`
--

CREATE TABLE `resposta` (
  `id` int(11) NOT NULL,
  `respondida` tinyint(1) NOT NULL,
  `questionario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `roteiro`
--

CREATE TABLE `roteiro` (
  `ID` int(11) NOT NULL,
  `Nome` varchar(255) NOT NULL,
  `Descricao` longtext NOT NULL,
  `ano` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `CoordenadorUtilizadorID` int(11) DEFAULT NULL,
  `diaAbertoID` int(11) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `roteiro`
--

INSERT INTO `roteiro` (`ID`, `Nome`, `Descricao`, `ano`, `created_at`, `CoordenadorUtilizadorID`, `diaAbertoID`, `updated_at`) VALUES
(2, 'Roteiro Teste', 'TEste 1234', 2022, '2024-04-23 21:26:57.560900', 41, 4, '2024-04-23 23:57:14.643393'),
(13, 'OLA', 'OLA', 2024, '2024-04-23 22:31:17.721769', 41, 6, '2024-04-23 22:45:37.823709'),
(24, 'FCT ROTEIRO', 'NAOSFJNAFKASFfffffffffffffffffffffsssssssssssssssssssssssssssssssssssssdjiasdifhouahfofhejnaewjlfn', 2024, '2024-04-24 14:25:49.791291', 41, 6, '2024-04-24 14:25:49.791291'),
(25, 'teste', 'teste', 2024, '2024-05-10 10:56:51.544880', 41, 6, '2024-05-14 18:38:49.484699');

-- --------------------------------------------------------

--
-- Estrutura da tabela `sala`
--

CREATE TABLE `sala` (
  `id` int(11) NOT NULL,
  `EspacoEdificio` varchar(255) NOT NULL,
  `EspacoID` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `sessao`
--

CREATE TABLE `sessao` (
  `ID` int(11) NOT NULL,
  `NInscritos` int(11) NOT NULL,
  `Vagas` int(11) NOT NULL,
  `Dia` date DEFAULT NULL,
  `AtividadeID` int(11) DEFAULT NULL,
  `HorarioID` int(11) NOT NULL,
  `RoteiroID` int(11) DEFAULT NULL,
  `nr_presentes` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `sessao`
--

INSERT INTO `sessao` (`ID`, `NInscritos`, `Vagas`, `Dia`, `AtividadeID`, `HorarioID`, `RoteiroID`, `nr_presentes`) VALUES
(30, 0, 45, '2022-05-03', 11, 19, NULL, 0),
(52, 0, 45, '2023-06-19', 10, 21, NULL, 0),
(26, 0, 45, '2022-05-03', 8, 20, NULL, 0),
(19, 0, 41, '2022-05-03', 7, 19, NULL, 0),
(24, 0, 45, '2022-05-03', 8, 19, NULL, 0),
(47, 0, 45, '2023-06-19', 12, 29, NULL, 0),
(29, 0, 45, '2022-05-04', 11, 19, NULL, 0),
(32, 0, 26, '2022-05-03', 13, 22, NULL, 0),
(33, 0, 45, '2022-05-04', 14, 20, NULL, 0),
(34, 0, 29, '2022-05-03', 15, 21, NULL, 0),
(35, 0, 30, '2022-05-04', 15, 21, NULL, 0),
(36, 0, 45, '2022-05-03', 16, 20, NULL, 0),
(37, 0, 45, '2022-05-04', 17, 19, NULL, 0),
(38, 0, 45, '2022-05-04', 18, 20, NULL, 0),
(39, 0, 45, '2022-05-03', 19, 19, NULL, 0),
(40, 0, 45, '2022-05-04', 19, 19, NULL, 0),
(46, 0, 45, '2023-06-18', 12, 14, NULL, 0),
(45, 0, 20, '2022-05-04', 21, 28, NULL, 0),
(50, 0, 45, '2023-06-18', 22, 14, NULL, 0),
(51, 0, 45, '2023-06-18', 22, 29, NULL, 0),
(58, 0, 30, '2024-04-25', NULL, 35, 2, 0),
(57, 0, 25, '2024-04-23', NULL, 34, 2, 0),
(71, 0, 25, '2024-06-29', NULL, 61, 25, 0),
(63, 0, 18, '2024-04-28', NULL, 48, 13, 0),
(70, 0, 8, '2024-04-28', NULL, 49, 24, 0),
(72, 0, 19, '2024-06-30', NULL, 51, 25, 0);

-- --------------------------------------------------------

--
-- Estrutura da tabela `tarefa`
--

CREATE TABLE `tarefa` (
  `ID` int(11) NOT NULL,
  `Nome` varchar(255) NOT NULL,
  `estado` varchar(64) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `dia` date NOT NULL,
  `horario` time(6) NOT NULL,
  `ColaboradorUtilizadorID` int(11) DEFAULT NULL,
  `CoordenadorUtilizadorID` int(11) DEFAULT NULL,
  `Diaaberto` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `tarefaacompanhar`
--

CREATE TABLE `tarefaacompanhar` (
  `tarefaid` int(11) NOT NULL,
  `origem` varchar(255) NOT NULL,
  `destino` varchar(255) NOT NULL,
  `inscricao` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `tarefaauxiliar`
--

CREATE TABLE `tarefaauxiliar` (
  `tarefaid` int(11) NOT NULL,
  `sessao` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `tarefaoutra`
--

CREATE TABLE `tarefaoutra` (
  `tarefaid` int(11) NOT NULL,
  `descricao` longtext NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `tema`
--

CREATE TABLE `tema` (
  `ID` int(11) NOT NULL,
  `Tema` varchar(64) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `tema`
--

INSERT INTO `tema` (`ID`, `Tema`) VALUES
(4, 'Área: Artes, Comunicação e Património'),
(5, 'Área: Ciências Sociais e da Educação'),
(6, 'Área: Ciências Exatas e Naturais'),
(7, 'Área: Ciências e Tecnologias da Saúde'),
(8, 'Área: Engenharias e Tecnologias'),
(9, 'Área: Economia, Gestão e Turismo');

-- --------------------------------------------------------

--
-- Estrutura da tabela `temaquestionario`
--

CREATE TABLE `temaquestionario` (
  `ID` int(11) NOT NULL,
  `Tema` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `temaquestionario`
--

INSERT INTO `temaquestionario` (`ID`, `Tema`) VALUES
(1, 'TEMA 1');

-- --------------------------------------------------------

--
-- Estrutura da tabela `transporte`
--

CREATE TABLE `transporte` (
  `ID` int(11) NOT NULL,
  `Identificador` varchar(32) NOT NULL,
  `Dia` date NOT NULL,
  `diaAberto` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `transporte`
--

INSERT INTO `transporte` (`ID`, `Identificador`, `Dia`, `diaAberto`) VALUES
(2, 'Autocarro 1', '2023-12-06', 4),
(3, 'Autocarro 2', '2023-12-06', 4),
(4, 'Autocarro 3', '2022-05-03', 3),
(5, 'Autocarro 4', '2022-05-03', 3),
(6, 'Autocarro 5', '2022-05-03', 3),
(7, 'Autocarro 6', '2022-05-03', 3),
(8, 'Autocarro 14', '2022-05-03', 3);

-- --------------------------------------------------------

--
-- Estrutura da tabela `transportehorario`
--

CREATE TABLE `transportehorario` (
  `ID` int(11) NOT NULL,
  `Origem` varchar(32) NOT NULL,
  `Chegada` varchar(32) NOT NULL,
  `HoraPartida` time(6) NOT NULL,
  `HoraChegada` time(6) NOT NULL,
  `Transporte` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `transportehorario`
--

INSERT INTO `transportehorario` (`ID`, `Origem`, `Chegada`, `HoraPartida`, `HoraChegada`, `Transporte`) VALUES
(3, 'Terminal', 'Penha', '08:25:00.000000', '08:50:00.000000', 2),
(7, 'Terminal', 'Gambelas', '08:25:00.000000', '08:50:00.000000', 5),
(5, 'Terminal', 'Penha', '08:25:00.000000', '08:50:00.000000', 3),
(6, 'Terminal', 'Gambelas', '08:25:00.000000', '08:50:00.000000', 4),
(8, 'Terminal', 'Penha', '08:45:00.000000', '09:05:00.000000', 6),
(9, 'Terminal', 'Gambelas', '08:45:00.000000', '09:05:00.000000', 7),
(10, 'Terminal', 'Gambelas', '09:00:00.000000', '09:20:00.000000', 2),
(11, 'Terminal', 'Gambelas', '09:00:00.000000', '09:20:00.000000', 3),
(12, 'Terminal', 'Penha', '09:00:00.000000', '09:20:00.000000', 4),
(13, 'Terminal', 'Penha', '09:00:00.000000', '09:20:00.000000', 5),
(14, 'Terminal', 'Gambelas', '09:15:00.000000', '09:30:00.000000', 6),
(15, 'Terminal', 'Penha', '09:15:00.000000', '09:25:00.000000', 7),
(16, 'Terminal', 'Penha', '09:45:00.000000', '10:00:00.000000', 2),
(17, 'Terminal', 'Penha', '09:45:00.000000', '10:00:00.000000', 3),
(18, 'Terminal', 'Gambelas', '06:45:00.000000', '10:00:00.000000', 4),
(19, 'Terminal', 'Gambelas', '09:45:00.000000', '10:00:00.000000', 5),
(20, 'Terminal', 'Penha', '10:25:00.000000', '10:40:00.000000', 6),
(21, 'Terminal', 'Gambelas', '10:25:00.000000', '10:40:00.000000', 7),
(22, 'Terminal', 'Gambelas', '12:25:00.000000', '12:40:00.000000', 2),
(23, 'Terminal', 'Penha', '12:25:00.000000', '12:40:00.000000', 3),
(24, 'Gambelas', 'Terminal', '17:26:00.000000', '18:29:00.000000', 8),
(25, 'Terminal', 'Gambelas', '08:25:00.000000', '08:50:00.000000', 2);

-- --------------------------------------------------------

--
-- Estrutura da tabela `transporteuniversitario`
--

CREATE TABLE `transporteuniversitario` (
  `Transporte` int(11) NOT NULL,
  `Capacidade` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `transporteuniversitario`
--

INSERT INTO `transporteuniversitario` (`Transporte`, `Capacidade`) VALUES
(2, 50),
(3, 50),
(4, 50),
(5, 50),
(6, 50),
(7, 50),
(8, 50);

-- --------------------------------------------------------

--
-- Estrutura da tabela `unidadeorganica`
--

CREATE TABLE `unidadeorganica` (
  `ID` int(11) NOT NULL,
  `Nome` varchar(255) NOT NULL,
  `Sigla` varchar(255) NOT NULL,
  `CampusID` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `unidadeorganica`
--

INSERT INTO `unidadeorganica` (`ID`, `Nome`, `Sigla`, `CampusID`) VALUES
(1, 'Escola Superior de Educação e Comunicação', 'ESEC', 1),
(2, 'Escola Superior de Gestão Hotelaria e Turismo', 'ESGHT', 3),
(3, 'Escola Superior de Saúde', 'ESS', 2),
(4, 'Instituto Superior de Engenharia', 'ISE', 1),
(5, 'Faculdade de Ciências Humanas e Sociais', 'FCHS', 2),
(6, 'Faculdade de Ciências e Tecnologia', 'FCT', 2),
(7, 'Faculdade de Economia', 'FE', 2),
(8, 'Faculdade de Medicina e Ciências Biomédicas', 'FMCB', 2),
(9, 'Desporto AAUAlg', 'GDAAUAlg', 1),
(10, 'Desporto AAUAlg', 'GDAAUAlg', 2),
(11, 'Biblioteca', 'BibPenha', 1),
(12, 'Biblioteca', 'BibGambelas', 2),
(13, 'Gabinete de Comunicação e Protocolo', 'GCP', 2);

-- --------------------------------------------------------

--
-- Estrutura da tabela `utilizador`
--

CREATE TABLE `utilizador` (
  `user_ptr_id` int(11) NOT NULL,
  `contacto` varchar(20) NOT NULL,
  `valido` varchar(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Extraindo dados da tabela `utilizador`
--

INSERT INTO `utilizador` (`user_ptr_id`, `contacto`, `valido`) VALUES
(1, '', 'True'),
(38, '+351919999999', 'True'),
(37, '+351966934582', 'True'),
(36, '+351914815430', 'True'),
(35, '+351914815430', 'True'),
(34, '+351961384454', 'True'),
(33, '+351963107359', 'True'),
(32, '+351914176692', 'True'),
(29, '+351917502181', 'True'),
(31, '+351919048144', 'True'),
(23, '+351963107359', 'True'),
(28, '+351936362302', 'True'),
(26, '+351919048144', 'True'),
(25, '+351919910008', 'True'),
(39, '+351919999999', 'Rejeitado'),
(40, '+351919191919', 'True'),
(41, '+351922262501', 'True');

--
-- Índices para tabelas despejadas
--

--
-- Índices para tabela `administrador`
--
ALTER TABLE `administrador`
  ADD PRIMARY KEY (`utilizador_ptr_id`);

--
-- Índices para tabela `anfiteatro`
--
ALTER TABLE `anfiteatro`
  ADD PRIMARY KEY (`EspacoID`);

--
-- Índices para tabela `arlivre`
--
ALTER TABLE `arlivre`
  ADD PRIMARY KEY (`EspacoID`);

--
-- Índices para tabela `atividade`
--
ALTER TABLE `atividade`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Atividade_Tema_ab8f2b29_fk_Tema_ID` (`Tema`),
  ADD KEY `Atividade_diaAbertoID_7b531386_fk_DiaAberto_ID` (`diaAbertoID`),
  ADD KEY `Atividade_EspacoID_131bf78a_fk_Espaco_ID` (`EspacoID`),
  ADD KEY `Atividade_ProfessorUniversitar_dc191844_fk_Professor` (`ProfessorUniversitarioUtilizadorID`);

--
-- Índices para tabela `atividaderoteiro`
--
ALTER TABLE `atividaderoteiro`
  ADD PRIMARY KEY (`id`);

--
-- Índices para tabela `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Índices para tabela `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  ADD KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`);

--
-- Índices para tabela `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  ADD KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`);

--
-- Índices para tabela `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Índices para tabela `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_user_id_6a12ed8b` (`user_id`),
  ADD KEY `auth_user_groups_group_id_97559544` (`group_id`);

--
-- Índices para tabela `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permissions_user_id_a95ead1b` (`user_id`),
  ADD KEY `auth_user_user_permissions_permission_id_1fbb5f2c` (`permission_id`);

--
-- Índices para tabela `campus`
--
ALTER TABLE `campus`
  ADD PRIMARY KEY (`ID`);

--
-- Índices para tabela `colaborador`
--
ALTER TABLE `colaborador`
  ADD PRIMARY KEY (`utilizador_ptr_id`),
  ADD KEY `Colaborador_curso_id_31076750` (`curso_id`),
  ADD KEY `Colaborador_departamento_id_029b91e9` (`departamento_id`),
  ADD KEY `Colaborador_faculdade_id_f4b0ed52` (`faculdade_id`);

--
-- Índices para tabela `colaboradorhorario`
--
ALTER TABLE `colaboradorhorario`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `ColaboradorHorario_ColaboradorUtilizadorID_c2215826` (`ColaboradorUtilizadorID`);

--
-- Índices para tabela `coordenador`
--
ALTER TABLE `coordenador`
  ADD PRIMARY KEY (`utilizador_ptr_id`),
  ADD KEY `Coordenador_DepartamentoID_77f7eb1c` (`DepartamentoID`),
  ADD KEY `Coordenador_FaculdadeID_49668228` (`FaculdadeID`);

--
-- Índices para tabela `curso`
--
ALTER TABLE `curso`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Curso_Unidadeorganica_48c855bd` (`Unidadeorganica`);

--
-- Índices para tabela `departamento`
--
ALTER TABLE `departamento`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Departamento_UnidadeOrganicaID_8b27b79e` (`UnidadeOrganicaID`);

--
-- Índices para tabela `diaaberto`
--
ALTER TABLE `diaaberto`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `DiaAberto_AdministradorUtilizadorID_6d32149b` (`AdministradorUtilizadorID`);

--
-- Índices para tabela `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6` (`user_id`);

--
-- Índices para tabela `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Índices para tabela `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Índices para tabela `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Índices para tabela `edificio`
--
ALTER TABLE `edificio`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Edificio_Campus_91396335` (`Campus`);

--
-- Índices para tabela `escola`
--
ALTER TABLE `escola`
  ADD PRIMARY KEY (`id`);

--
-- Índices para tabela `espaco`
--
ALTER TABLE `espaco`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Espaco_Edificio_2d36e7bd` (`Edificio`);

--
-- Índices para tabela `estado`
--
ALTER TABLE `estado`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Estado_questionario_id_cd34d0e1_fk_Questionario_id` (`questionario_id`);

--
-- Índices para tabela `horario`
--
ALTER TABLE `horario`
  ADD PRIMARY KEY (`ID`);

--
-- Índices para tabela `idioma`
--
ALTER TABLE `idioma`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Idioma_DiaAbertoID_05e90160` (`DiaAbertoID`);

--
-- Índices para tabela `informacaomensagem`
--
ALTER TABLE `informacaomensagem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `InformacaoMensagem_data_b36b7c63` (`data`),
  ADD KEY `InformacaoMensagem_emissorid_a39368ba` (`emissorid`),
  ADD KEY `InformacaoMensagem_recetorid_90645bfe` (`recetorid`);

--
-- Índices para tabela `informacaonotificacao`
--
ALTER TABLE `informacaonotificacao`
  ADD PRIMARY KEY (`id`),
  ADD KEY `InformacaoNotificacao_data_52dada64` (`data`),
  ADD KEY `InformacaoNotificacao_emissorid_45bdccef` (`emissorid`),
  ADD KEY `InformacaoNotificacao_recetorid_343e36f0` (`recetorid`);

--
-- Índices para tabela `inscricao`
--
ALTER TABLE `inscricao`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Inscricao_diaaberto_id_4be8f9d7` (`diaaberto_id`),
  ADD KEY `Inscricao_escola_id_ea15d710` (`escola_id`),
  ADD KEY `Inscricao_participante_id_1d4e1894` (`participante_id`);

--
-- Índices para tabela `inscricaoprato`
--
ALTER TABLE `inscricaoprato`
  ADD PRIMARY KEY (`id`),
  ADD KEY `InscricaoPrato_campus_id_a9d69a78` (`campus_id`),
  ADD KEY `InscricaoPrato_inscricao_id_287b42e4` (`inscricao_id`);

--
-- Índices para tabela `inscricaosessao`
--
ALTER TABLE `inscricaosessao`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `InscricaoSessao_inscricao_id_sessao_id_113816db_uniq` (`inscricao_id`,`sessao_id`),
  ADD KEY `InscricaoSessao_inscricao_id_8c9294c7` (`inscricao_id`),
  ADD KEY `InscricaoSessao_sessao_id_f35a89a7` (`sessao_id`);

--
-- Índices para tabela `inscricaotransporte`
--
ALTER TABLE `inscricaotransporte`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `InscricaoTransporte_inscricao_id_transporte_id_0271b0c8_uniq` (`inscricao_id`,`transporte_id`),
  ADD KEY `InscricaoTransporte_inscricao_id_e344f36a` (`inscricao_id`),
  ADD KEY `InscricaoTransporte_transporte_id_c07ff887` (`transporte_id`);

--
-- Índices para tabela `materiais`
--
ALTER TABLE `materiais`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Materiais_AtividadeID_8a288a96` (`AtividadeID`);

--
-- Índices para tabela `mensagemenviada`
--
ALTER TABLE `mensagemenviada`
  ADD PRIMARY KEY (`id`),
  ADD KEY `MensagemEnviada_mensagem_id_650a9228` (`mensagem_id`);

--
-- Índices para tabela `mensagemrecebida`
--
ALTER TABLE `mensagemrecebida`
  ADD PRIMARY KEY (`id`),
  ADD KEY `MensagemRecebida_mensagem_id_929cdaa9` (`mensagem_id`);

--
-- Índices para tabela `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `Menu_Campus_diaAberto_Dia_a69897bd_uniq` (`Campus`,`diaAberto`,`Dia`),
  ADD KEY `Menu_Campus_86dfb9c3` (`Campus`),
  ADD KEY `Menu_diaAberto_ad0e738c` (`diaAberto`),
  ADD KEY `Menu_HorarioID_c27c1815` (`HorarioID`);

--
-- Índices para tabela `notificacao`
--
ALTER TABLE `notificacao`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Notificacao_unread_5c525732` (`unread`),
  ADD KEY `Notificacao_timestamp_b0c7de17` (`timestamp`),
  ADD KEY `Notificacao_public_e83b3bfc` (`public`),
  ADD KEY `Notificacao_deleted_5e8a8468` (`deleted`),
  ADD KEY `Notificacao_emailed_a50d3d89` (`emailed`),
  ADD KEY `Notificacao_action_object_content_type_id_5bed7a4d` (`action_object_content_type_id`),
  ADD KEY `Notificacao_actor_content_type_id_247a4ff9` (`actor_content_type_id`),
  ADD KEY `Notificacao_recipient_id_0202c4a6` (`recipient_id`),
  ADD KEY `Notificacao_target_content_type_id_eb8c11a8` (`target_content_type_id`),
  ADD KEY `Notificacao_recipient_id_unread_4902da17_idx` (`recipient_id`,`unread`);

--
-- Índices para tabela `opcaoresposta`
--
ALTER TABLE `opcaoresposta`
  ADD PRIMARY KEY (`id`);

--
-- Índices para tabela `participante`
--
ALTER TABLE `participante`
  ADD PRIMARY KEY (`utilizador_ptr_id`);

--
-- Índices para tabela `pergunta`
--
ALTER TABLE `pergunta`
  ADD PRIMARY KEY (`id`);

--
-- Índices para tabela `prato`
--
ALTER TABLE `prato`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Prato_MenuID_c8d51dba` (`MenuID`);

--
-- Índices para tabela `preferencia`
--
ALTER TABLE `preferencia`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Preferencia_ColaboradorUtilizadorID_5d7e095c` (`ColaboradorUtilizadorID`);

--
-- Índices para tabela `preferenciaatividade`
--
ALTER TABLE `preferenciaatividade`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `PreferenciaAtividade_Atividade_8a2c1f3d` (`Atividade`),
  ADD KEY `PreferenciaAtividade_PreferenciaID_8e4d7536` (`PreferenciaID`);

--
-- Índices para tabela `professoruniversitario`
--
ALTER TABLE `professoruniversitario`
  ADD PRIMARY KEY (`utilizador_ptr_id`),
  ADD KEY `ProfessorUniversitario_departamento_id_bae8bcc3` (`departamento_id`),
  ADD KEY `ProfessorUniversitario_faculdade_id_21325caa` (`faculdade_id`);

--
-- Índices para tabela `questionario`
--
ALTER TABLE `questionario`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Questionario_estado_id_0f63af8c_fk_Estado_id` (`estado_id`);

--
-- Índices para tabela `responsavel`
--
ALTER TABLE `responsavel`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Responsavel_inscricao_id_62b18f0c` (`inscricao_id`);

--
-- Índices para tabela `resposta`
--
ALTER TABLE `resposta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Resposta_questionario_id_0abca127_fk_Questionario_id` (`questionario_id`);

--
-- Índices para tabela `roteiro`
--
ALTER TABLE `roteiro`
  ADD PRIMARY KEY (`ID`);

--
-- Índices para tabela `sala`
--
ALTER TABLE `sala`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Sala_EspacoID_c91a0491` (`EspacoID`);

--
-- Índices para tabela `sessao`
--
ALTER TABLE `sessao`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Sessao_AtividadeID_0931b4e1` (`AtividadeID`),
  ADD KEY `Sessao_HorarioID_beea39cb` (`HorarioID`),
  ADD KEY `Sessao_RoteiroID_a4bb1d0b` (`RoteiroID`);

--
-- Índices para tabela `tarefa`
--
ALTER TABLE `tarefa`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Tarefa_ColaboradorUtilizadorID_82eab2cc` (`ColaboradorUtilizadorID`),
  ADD KEY `Tarefa_CoordenadorUtilizadorID_9e97a908` (`CoordenadorUtilizadorID`),
  ADD KEY `Tarefa_Diaaberto_8188b58c` (`Diaaberto`);

--
-- Índices para tabela `tarefaacompanhar`
--
ALTER TABLE `tarefaacompanhar`
  ADD PRIMARY KEY (`tarefaid`),
  ADD KEY `TarefaAcompanhar_inscricao_caba3aa9` (`inscricao`);

--
-- Índices para tabela `tarefaauxiliar`
--
ALTER TABLE `tarefaauxiliar`
  ADD PRIMARY KEY (`tarefaid`),
  ADD KEY `TarefaAuxiliar_sessao_585ae447` (`sessao`);

--
-- Índices para tabela `tarefaoutra`
--
ALTER TABLE `tarefaoutra`
  ADD PRIMARY KEY (`tarefaid`);

--
-- Índices para tabela `tema`
--
ALTER TABLE `tema`
  ADD PRIMARY KEY (`ID`);

--
-- Índices para tabela `temaquestionario`
--
ALTER TABLE `temaquestionario`
  ADD PRIMARY KEY (`ID`);

--
-- Índices para tabela `transporte`
--
ALTER TABLE `transporte`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Transporte_diaAberto_d2f61ae1` (`diaAberto`);

--
-- Índices para tabela `transportehorario`
--
ALTER TABLE `transportehorario`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `TransporteHorario_Transporte_18a4877f` (`Transporte`);

--
-- Índices para tabela `transporteuniversitario`
--
ALTER TABLE `transporteuniversitario`
  ADD PRIMARY KEY (`Transporte`);

--
-- Índices para tabela `unidadeorganica`
--
ALTER TABLE `unidadeorganica`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `UnidadeOrganica_CampusID_2e2e86da` (`CampusID`);

--
-- Índices para tabela `utilizador`
--
ALTER TABLE `utilizador`
  ADD PRIMARY KEY (`user_ptr_id`);

--
-- AUTO_INCREMENT de tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `atividade`
--
ALTER TABLE `atividade`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT de tabela `atividaderoteiro`
--
ALTER TABLE `atividaderoteiro`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT de tabela `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de tabela `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=237;

--
-- AUTO_INCREMENT de tabela `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT de tabela `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT de tabela `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `campus`
--
ALTER TABLE `campus`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de tabela `colaboradorhorario`
--
ALTER TABLE `colaboradorhorario`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de tabela `curso`
--
ALTER TABLE `curso`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- AUTO_INCREMENT de tabela `departamento`
--
ALTER TABLE `departamento`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT de tabela `diaaberto`
--
ALTER TABLE `diaaberto`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de tabela `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=60;

--
-- AUTO_INCREMENT de tabela `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=59;

--
-- AUTO_INCREMENT de tabela `edificio`
--
ALTER TABLE `edificio`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de tabela `escola`
--
ALTER TABLE `escola`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de tabela `espaco`
--
ALTER TABLE `espaco`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=66;

--
-- AUTO_INCREMENT de tabela `estado`
--
ALTER TABLE `estado`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `horario`
--
ALTER TABLE `horario`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;

--
-- AUTO_INCREMENT de tabela `idioma`
--
ALTER TABLE `idioma`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `informacaomensagem`
--
ALTER TABLE `informacaomensagem`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de tabela `informacaonotificacao`
--
ALTER TABLE `informacaonotificacao`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=92;

--
-- AUTO_INCREMENT de tabela `inscricao`
--
ALTER TABLE `inscricao`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de tabela `inscricaoprato`
--
ALTER TABLE `inscricaoprato`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de tabela `inscricaosessao`
--
ALTER TABLE `inscricaosessao`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de tabela `inscricaotransporte`
--
ALTER TABLE `inscricaotransporte`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `materiais`
--
ALTER TABLE `materiais`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT de tabela `mensagemenviada`
--
ALTER TABLE `mensagemenviada`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de tabela `mensagemrecebida`
--
ALTER TABLE `mensagemrecebida`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de tabela `menu`
--
ALTER TABLE `menu`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de tabela `notificacao`
--
ALTER TABLE `notificacao`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=78;

--
-- AUTO_INCREMENT de tabela `opcaoresposta`
--
ALTER TABLE `opcaoresposta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `pergunta`
--
ALTER TABLE `pergunta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `prato`
--
ALTER TABLE `prato`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de tabela `preferencia`
--
ALTER TABLE `preferencia`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de tabela `preferenciaatividade`
--
ALTER TABLE `preferenciaatividade`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de tabela `questionario`
--
ALTER TABLE `questionario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `responsavel`
--
ALTER TABLE `responsavel`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de tabela `resposta`
--
ALTER TABLE `resposta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `roteiro`
--
ALTER TABLE `roteiro`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT de tabela `sala`
--
ALTER TABLE `sala`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `sessao`
--
ALTER TABLE `sessao`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=80;

--
-- AUTO_INCREMENT de tabela `tarefa`
--
ALTER TABLE `tarefa`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de tabela `tema`
--
ALTER TABLE `tema`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de tabela `temaquestionario`
--
ALTER TABLE `temaquestionario`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de tabela `transporte`
--
ALTER TABLE `transporte`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de tabela `transportehorario`
--
ALTER TABLE `transportehorario`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de tabela `unidadeorganica`
--
ALTER TABLE `unidadeorganica`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Restrições para despejos de tabelas
--

--
-- Limitadores para a tabela `estado`
--
ALTER TABLE `estado`
  ADD CONSTRAINT `Estado_questionario_id_cd34d0e1_fk_Questionario_id` FOREIGN KEY (`questionario_id`) REFERENCES `questionario` (`id`);

--
-- Limitadores para a tabela `questionario`
--
ALTER TABLE `questionario`
  ADD CONSTRAINT `Questionario_estado_id_0f63af8c_fk_Estado_id` FOREIGN KEY (`estado_id`) REFERENCES `estado` (`id`);

--
-- Limitadores para a tabela `resposta`
--
ALTER TABLE `resposta`
  ADD CONSTRAINT `Resposta_questionario_id_0abca127_fk_Questionario_id` FOREIGN KEY (`questionario_id`) REFERENCES `questionario` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
