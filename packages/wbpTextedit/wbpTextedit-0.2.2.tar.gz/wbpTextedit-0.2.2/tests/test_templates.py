from wbBase.application import App
from wbBase.applicationInfo import ApplicationInfo, PluginInfo
from wbpTextedit.template import PlainTextTemplate
from wbpTextedit.template.ini import IniTextTemplate
from wbpTextedit.template.python import PythonTextTemplate
from wbpTextedit.template.xml import XMLTextTemplate

appinfo = ApplicationInfo(Plugins=[PluginInfo(Name="textedit", Installation="default")])


def test_plugin():
    app = App(test=True, info=appinfo)
    assert "textedit" in app.pluginManager
    app.Destroy()


def test_PlainTextTemplate():
    app = App(test=True, info=appinfo)
    assert any(isinstance(t, PlainTextTemplate) for t in app.documentManager.templates)
    assert any(
        isinstance(t, PlainTextTemplate) for t in app.documentManager.visibleTemplates
    )
    assert any(
        isinstance(t, PlainTextTemplate) for t in app.documentManager.newableTemplates
    )
    assert isinstance(
        app.documentManager.FindTemplateByType(PlainTextTemplate), PlainTextTemplate
    )
    assert isinstance(
        app.documentManager.FindTemplateByDocumentTypeName("PlainTextDocument"),
        PlainTextTemplate,
    )
    assert isinstance(
        app.documentManager.FindTemplateForPath("test.txt"), PlainTextTemplate
    )
    app.Destroy()


def test_IniTextTemplate():
    app = App(test=True, info=appinfo)
    assert any(isinstance(t, IniTextTemplate) for t in app.documentManager.templates)
    assert any(
        isinstance(t, IniTextTemplate) for t in app.documentManager.visibleTemplates
    )
    assert any(
        isinstance(t, IniTextTemplate) for t in app.documentManager.newableTemplates
    )
    assert isinstance(
        app.documentManager.FindTemplateByType(IniTextTemplate), IniTextTemplate
    )
    assert isinstance(
        app.documentManager.FindTemplateByDocumentTypeName("Config File"),
        IniTextTemplate,
    )
    assert isinstance(
        app.documentManager.FindTemplateForPath("test.ini"), IniTextTemplate
    )
    assert isinstance(
        app.documentManager.FindTemplateForPath("test.cfg"), IniTextTemplate
    )
    app.Destroy()


def test_PythonTextTemplate():
    app = App(test=True, info=appinfo)
    assert any(isinstance(t, PythonTextTemplate) for t in app.documentManager.templates)
    assert any(
        isinstance(t, PythonTextTemplate) for t in app.documentManager.visibleTemplates
    )
    assert any(
        isinstance(t, PythonTextTemplate) for t in app.documentManager.newableTemplates
    )
    assert isinstance(
        app.documentManager.FindTemplateByType(PythonTextTemplate), PythonTextTemplate
    )
    assert isinstance(
        app.documentManager.FindTemplateByDocumentTypeName("Python Script"),
        PythonTextTemplate,
    )
    assert isinstance(
        app.documentManager.FindTemplateForPath("test.py"), PythonTextTemplate
    )
    assert isinstance(
        app.documentManager.FindTemplateForPath("test.pyw"), PythonTextTemplate
    )
    app.Destroy()


def test_XMLTextTemplate():
    app = App(test=True, info=appinfo)
    assert any(isinstance(t, XMLTextTemplate) for t in app.documentManager.templates)
    assert any(
        isinstance(t, XMLTextTemplate) for t in app.documentManager.visibleTemplates
    )
    assert any(
        isinstance(t, XMLTextTemplate) for t in app.documentManager.newableTemplates
    )
    assert isinstance(
        app.documentManager.FindTemplateByType(XMLTextTemplate), XMLTextTemplate
    )
    assert isinstance(
        app.documentManager.FindTemplateByDocumentTypeName("XML Text"), XMLTextTemplate
    )
    assert isinstance(
        app.documentManager.FindTemplateForPath("test.xml"), XMLTextTemplate
    )
    assert isinstance(
        app.documentManager.FindTemplateForPath("test.xsd"), XMLTextTemplate
    )
    app.Destroy()
