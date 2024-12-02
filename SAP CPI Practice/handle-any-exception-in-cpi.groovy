import com.sap.gateway.ip.core.customdev.util.Message

def Message processData(Message message) {
    def map = message.getProperties();
    def ex = map.get("CamelExceptionCaught");

    if (ex != null) {
        def messageLog = messageLogFactory.getMessageLog(message);

        // Log exception details
        if (messageLog != null) {
            messageLog.addAttachmentAsString("Exception Class", ex.getClass().getCanonicalName(), "text/plain");
            messageLog.addAttachmentAsString("Exception Message", ex.getMessage(), "text/plain");
            messageLog.addAttachmentAsString("Exception Stack Trace", ex.getStackTrace().toString(), "text/plain");
        }

        // Store exception details in message properties
        message.setProperty("ExceptionClass", ex.getClass().getCanonicalName());
        message.setProperty("ExceptionMessage", ex.getMessage());
        message.setProperty("ExceptionStackTrace", ex.getStackTrace().toString());

        // Handle specific exception types
        if (ex instanceof org.apache.camel.component.ahc.AhcOperationFailedException) {
            def ahcEx = ex as org.apache.camel.component.ahc.AhcOperationFailedException;
            
            if (messageLog != null) {
                messageLog.addAttachmentAsString("http.ResponseBody", ahcEx.getResponseBody(), "text/plain");
            }
            
            message.setProperty("http.ResponseBody", ahcEx.getResponseBody());
            message.setProperty("http.StatusCode", ahcEx.getStatusCode());
            message.setProperty("http.StatusText", ahcEx.getStatusText());
            message.setBody(ahcEx.getResponseBody());
        } else {
            // Default handling for other exception types
            message.setBody("Exception occurred: " + ex.getMessage());
        }
    }

    return message;
}
