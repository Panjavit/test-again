module ku.cs {
    requires javafx.controls;
    requires javafx.fxml;


    opens ku.cs.controllers to javafx.fxml;
    exports ku.cs.controllers;
    exports ku.cs.lab03javafx;
    opens ku.cs.lab03javafx to javafx.fxml;
}