from enum import Enum
import jpype

import aspose.models
from aspose import helper


class PreprocessingFilter(helper.BaseJavaClass):
    """
    Base class for image processing commands.
    """
    JAVA_CLASS_NAME = "com.aspose.ocr.PreprocessingFilter"
    def __init__(self):
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        self.__javaClass = asposeClass()
        self.__javaClassName = ""

        if self.__javaClassName == None or self.__javaClassName == "":
            self.__javaClassName = str(self.__javaClass.getClass().getName())

    def getJavaClass(self):
        return self.__javaClass

    @staticmethod
    def binarize():
        """
        Converts an image to black-and-white image.
        Binary images are images whose pixels have only two possible intensity values.
        They are normally displayed as black and white. Numerically, the two values are often 0 for black, and 255 for white.
        Binary images are produced by auto thresholding an image.
        @return: BinarizeFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.Binarize()

    @staticmethod
    def resize(width : int, height : int):
        """
        Rescale image - upscale or downscale image resolution.
        @param width: The new width of the image.
        @param height: The new height of the image.
        @return: ResizeFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.Resize(width, height)

    @staticmethod
    def binarize_and_dilate():
        """
        Dilation adds pixels to the boundaries of objects in an image.
        @return: DilateFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.BinarizeAndDilate()

    @staticmethod
    def invert():
        """
        Automatically inverts colors in a document image.
        @return: InvertFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.Invert()

    @staticmethod
    def rotate(angle : float):
        """
        Rotate original image.
        @param angle: Angle of rotation. Value from -360 to 360.
        @return: RotateFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.Rotate(angle)

    @staticmethod
    def scale(ratio : float):
        """
        Rescale image - Upscale or downscale image resolution.
        InterpolationFilterType bilinear or nearest neighbor.
        @param ratio: The scaling factor. Recommended value from 0.1 to 1 to shrink. From 1 to 10 to enlarge.
        @return: ScaleFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.Scale(ratio)

    @staticmethod
    def to_grayscale():
        """
        Converts an image to grayscale image.
        Grayscale image have 256 level of light in image (0 to 255).
        @return: GrayscaleFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.ToGrayscale()

    @staticmethod
    def threshold(value : int):
        """
        Create a binary image based on setting a threshold value on the pixel intensity of the original image.
        @param value: The max value.
        @return: BinarizeFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.Threshold(value)

    @staticmethod
    def median():
        """
        The median filter run through each element of the image and replace each pixel with the median of its neighboring pixels.
        @return: MedianFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.Median()

    @staticmethod
    def auto_denoising():
        """
        Enables the use of an additional neural network to improve the image - reduce noise.
        Useful for images with scan artifacts, distortion, spots, flares, gradients, foreign elements.
        @return: AutoDenoisingFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.AutoDenoising()

    @staticmethod
    def auto_dewarping():
        """
        Automatically corrects geometric distortions in the image.
        Extremely resource intensive!
        @return: AutoDewarpingFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.AutoDewarping()

    @staticmethod
    def auto_skew():
        """
        Enables the automatic image skew correction.
        @return: AutoSkewFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.AutoSkew()

    @staticmethod
    def contrast_correction():
        """
        Contrast correction filter.
        @return: ContrastCorrectionFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.ContrastCorrection()

    def add(self, filter):
        """
        Add filter to collection for further preprocessing.
        @param filter: PreprocessingFilter object.
        """
        self.getJavaClass().add(filter)



class InputType(Enum):
    """
    Types of image/ documents for processing / recognition.
    """
    SINGLE_IMAGE = 0
    """ Supports GIF, PNG, JPEG, BMP, TIFF, JFIF, binary array."""
    PDF = 1
    """ Scanned PDF document from file or from bynary array."""
    TIFF = 2
    """ Multipage TIFF, TIF document from file or from InputStream."""
    URL = 3
    """ Link on the image. Supports GIF, PNG, JPEG, BMP, TIFF."""
    DIRECTORY = 4
    """ Path to the directory. Nested archives and folders are not supported.
        Supports GIF, PNG, JPEG, BMP, TIFF.
        Default amount of processed images is all."""
    ZIP = 5
    """ Full name of the ZIP archive. Nested archives and folders are not supported.
        Supports GIF, PNG, JPEG, BMP, TIFF, JFIF.
        Default amount of processed images is all."""
    BASE64 = 6
    """ base64 string with the image or path to the .txt file with the base64 content. Supports GIF, PNG, JPEG, BMP, TIFF."""



class ImageData(helper.BaseJavaClass):
    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.initParams()

    def initParams(self):
        self.source = str(self.getJavaClass().Source);
        self.type = self.getJavaClass().Type;
        self.width = self.getJavaClass().Width;
        self.height = self.getJavaClass().Height;
        self.filters = self.getJavaClass().Filters;
        self.image = self.getJavaClass().Image;

class OcrInput():
    """
    Main class to collect images.
    """
    __JAVA_CLASS_NAME = "com.aspose.ocr.OcrInput"

    def __init__(self, type : InputType, filters : PreprocessingFilter = None):
        """
        Constructor to create container and set the type of images / documents and filters for further processing / recognition.
        @param type: Set the images/documents type will be added to container.
        @param filters: Set processing filters will be applied for further processing or recognition.
        """
        asposeClass = jpype.JClass(OcrInput.__JAVA_CLASS_NAME)
        jType = ModelsConverter.convertInputTypeToJava(type)
        if filters == None:
            self.__javaClass = asposeClass(jType)
        else:
            self.__javaClass = asposeClass(jType, filters.getJavaClass())
        self.__javaClassName = ""
        self.__stream = []
        self.type = type

        if self.__javaClassName == None or self.__javaClassName == "":
            self.__javaClassName = str(self.__javaClass.getClass().getName())

    def init(self, javaClass):
        self.__javaClass = javaClass

        self.source = self.__javaClass.get(0).Source


    def add(self, fullPath : str, startPage : int = None, pagesNumber: int = None):
        """
        Add the path or URI containing the image for recognition / processing.
        The type of the image must correspond to the type specified in the constructor.
        @param fullPath: Path to the image/ document / folder / archive.
        @param startPage: The first page/image for processing / recognition. Use for documents, zip, folders.
        @param pagesNumber: The total amount of pages/images for processing / recognition. Use for documents, zip, folders. Default = all.
        """
        if startPage == None or pagesNumber == None:
            self.__javaClass.add(fullPath)
        else:
            self.__javaClass.add(fullPath, startPage, pagesNumber)
        # if self.__type != None:
        #     self.__type =


    def addStream(self, image_data_binary, startPage: int = None, pagesNumber: int = None):
        """
        Add the InputStream containing the image for recognition / processing.
        The type of the image must correspond to the type specified in the constructor.

        \code
             input = OcrInput(InputType.SINGLE_IMAGE)
            file = open(imgPath, "rb")
            image_data_binary = file.read()
            file.close()
            input.addStream(image_data_binary)
            result = api.recognize(input, RecognitionSettings())
        \endcode

        @param image_data_binary: containing the image or document.
        @param startPage: The first page/image for processing / recognition. Use for documents, zip, folders.
        @param pagesNumber: The total amount of pages/images for processing / recognition. Use for documents, zip, folders. Default = all.
        """
        stream = jpype.JClass('java.io.ByteArrayInputStream')
        streamJava = stream(image_data_binary)
        if startPage == None or pagesNumber == None:
            self.__javaClass.add(streamJava)
        else:
            self.__javaClass.add(streamJava, startPage, pagesNumber)

        self.__stream.append(image_data_binary)

    def add_base64(self, base64 : str):
        """
        Add the base64 string containing the image for recognition / processing.
        The type of the image must correspond to the type specified in the constructor.
        @param base64: Base64 string with single image.
        """
        self.__javaClass.addBase64(base64)

    def clear(self):
        """
        Set the amount of items for processing / recognition as 0.
        Clear the collection.
        """
        self.__javaClass.clear()

    def clear_filters(self):
        """
        Remove all filters.
        """
        self.__javaClass.clearFilters()

    def size(self):
        """
        Amount of items for processing / recognition.
        @return: Amount of items.
        """
        return self.__javaClass.size()

    def get(self, index : int) -> ImageData:
        """
        Returns information about processed / recognized image.
        @param index: Position of the image in the List.
        @return: The object of ImageData.
        """
        return ImageData(self.__javaClass.get(index))

    def getJavaClass(self):
        return self.__javaClass

class Format(Enum):
    """ Format to save recognition result as document. """
    TEXT = 0
    """ Saves the result in the plain text format. """
    DOCX = 1
    """ Saves the result as an Office Open XML Word processing ML Document (macro-free). """
    PDF = 2
    """ Saves the result as a PDF (Adobe Portable Document) Document. """
    XLSX = 3
    """ Saves the result as an Excel ( 2007 and later) workbook Document. """
    XML = 4
    """ Saves the result as an XML Document. """
    JSON = 5
    """ Saves the result as an plain text written in JavaScript object notation. """
    HTML = 6
    """ Saves the document as an HTML file. """
    EPUB = 7
    """ Saves the document as an EPUB file. """
    RTF = 8
    """ Saves the document as an rtf file. """
    PDF_NO_IMG = 9
    """ Saves the document as a Searchable PDF (Adobe Portable Document) Document without image. """


class SpellCheckLanguage(Enum):
    """ Dictionary language for spell-check correction. """
    ENG = 0
    """ English dictionary """
    DEU = 1
    """ German dictionary """
    SPA = 2
    """ Spanish dictionary """
    FRA = 3
    """ French dictionary """
    ITA = 4
    """ Italian dictionary """
    POR = 5
    """ Portuguese dictionary """
    CZE = 6
    """ Czech dictionary """
    DAN = 7
    """ Danish dictionary """
    DUM = 8
    """ Dutch dictionary """
    EST = 9
    """ Estonian dictionary """
    FIN = 10
    """ Finnish dictionary """
    LAV = 11
    """ Latvian dictionary """
    LIT = 12
    """ Lithuanian dictionary """
    POL = 13
    """ Polish dictionary """
    RUM = 14
    """ Romanian dictionary """
    SLK = 15
    """ Slovak dictionary """
    SLV = 16
    """ Slovene dictionary """
    SWE = 17
    """ Swedish dictionary """

class Language(Enum):
    """ Language model for the recognition. """
    NONE = 0
    """ Multi - language support """
    LATIN = 1
    """ Multi - language(latin alphabet) support """
    CYRILLIC = 2
    """ Multi - language(cyrillic alphabet) support """
    ENG = 3
    """ English alphabet """
    DEU = 4
    """ German alphabet """
    POR = 5
    """ Portuguese alphabet """
    SPA = 6
    """ Spanish alphabet """
    FRA = 7
    """ French alphabet """
    ITA = 8
    """ Italian alphabet """
    CZE = 9
    """ Czech alphabet """
    DAN = 10
    """ Danish alphabet """
    DUM = 11
    """ Dutch alphabet """
    EST = 12
    """ Estonian alphabet """
    FIN = 13
    """ Finnish alphabet """
    LAV = 14
    """ Latvian alphabet """
    LIT = 15
    """ Lithuanian alphabet """
    NOR = 16
    """ Norwegian alphabet """
    POL = 17
    """ Polish alphabet """
    RUM = 18
    """ Romanian alphabet """
    SRP_HRV = 19
    """ Serbo-Croatian alphabet """
    SLK = 20
    """ Slovak alphabet """
    SLV = 21
    """ Slovene alphabet """
    SWE = 22
    """ Swedish alphabet """
    CHI = 23
    """ Chinese alphabet """
    BEL = 24
    """ Belorussian alphabet """
    BUL = 25
    """ Bulgarian alphabet """
    KAZ = 26
    """ Kazakh alphabet """
    RUS = 27
    """ Russian alphabet """
    SRP = 28
    """ Serbian alphabet """
    UKR = 29
    """ Ukrainian alphabet """
    HIN = 30
    """ Hindi alphabet """


class DetectAreasMode(Enum):
    """
    Determines the type of neural network used for areas detection.
    Used in the RecognitionSettings to specify which type of image you want to recognize.
    """
    NONE = 0
    """ Doesn't detect paragraphs.
    Better for a simple one-column document without pictures. """
    DOCUMENT = 1
    """ Detects paragraphs uses NN model for documents. 
    Better for multicolumn document, document with pictures or with other not text objects. """
    PHOTO = 2
    """ Detects paragraphs uses NN model for photos. 
    Better for image with a lot of pictures and other not text objects. """
    COMBINE = 3
    """ Detects paragraphs with text and then uses other NN model to detect areas inside of paragraphs.
    Better for images with complex structure. """
    TABLE = 4
    """ Detects cells with text.
    Preferable mode for images with table structure. """
    CURVED_TEXT = 5
    """ Detects lines and recognizes text on curved images.
    Preferred mode for photos of book and magazine pages. """
    TEXT_IN_WILD = 6
    """ A super-powerful neural network specialized in extracting words from low-quality images such as street photos, license plates, passport photos, meter photos, and photos with noisy backgrounds. """

class AreasType(Enum):
    """ Determines the type of regions detected by the model.
    Used in the get_text_areas to indicate which result will be obtained - paragraph coordinates or line coordinates.
    """
    PARAGRAPHS = 0
    """ Sets regions as paragraphs """
    LINES = 1
    """ Sets regions as lines """
    WORDS = 2
    """ Sets regions as words """



class SpellCheckError(helper.BaseJavaClass):
    """
    Representing misspelled word with additional data.
    """
    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.suggested_words = []
        self.initParams()

    def initParams(self):
        self.word = self.getJavaClass().word
        """
        The word being misspelled.
        """
        self.start_position = self.getJavaClass().startPosition
        """
        Word's position in the input text.
        """
        self.length = self.getJavaClass().length
        """
        Misspelled word's length in the input text.
        """
        suggestion = self.getJavaClass().suggestedWords
        """
        list of objects with suggested correct spellings
        """
        for item in suggestion:
            self.suggested_words.append(SuggestedWord(item))


class SuggestedWord(helper.BaseJavaClass):
    """
    Spelling suggestion returned from get_spell_check_error_list.
    """
    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.initParams()

    def initParams(self):
        self.word = self.getJavaClass().word
        """
        The suggested correctly spelled word.
        """
        self.distance = self.getJavaClass().distance
        """
        The distance between the searched and suggestion.
        """




class ModelsConverter:

    def convertToJavaAreasType(jType):
        return ModelsConverter.__switchAreasType(jType)

    def __switchAreasType(type):
        javaType = "com.aspose.ocr.AreasType"
        areastype = jpype.JClass(javaType)
        if type.name == "PARAGRAPHS":
            return areastype.PARAGRAPHS
        if type.name == "LINES":
            return areastype.LINES
        if type.name == "WORDS":
            return areastype.WORDS

    def convertToJavaSpellCheckLanguage(jType):
        return ModelsConverter.__switchSpellCheckLanguage(jType)

    def __switchSpellCheckLanguage(type):
        javaType = "com.aspose.ocr.SpellCheck.SpellCheckLanguage"
        language = jpype.JClass(javaType)
        if type.name == "ENG":
            return language.Eng
        elif type.name == "DEU":
            return language.Deu
        if type.name =="SPA":
            return language.Spa
        if type.name =="FRA":
            return language.Fra
        if type.name =="ITA":
            return language.Ita
        if type.name =="POR":
            return language.Por
        if type.name =="CZE":
            return language.Cze
        if type.name =="DAN":
            return language.Dan
        if type.name =="DUM":
            return language.Dum
        if type.name =="EST":
            return language.Est
        if type.name =="FIN":
            return language.Fin
        if type.name =="LAV":
            return language.Lav
        if type.name =="LIT":
            return language.Lit
        if type.name =="POL":
            return language.Pol
        if type.name =="RUM":
            return language.Rum
        if type.name =="SLK":
            return language.Slk
        if type.name =="SLV":
            return language.Slv
        if type.name =="SWE":
            return language.Swe

    def convertToJavaFormat(jType):
        return ModelsConverter.__switchFormat(jType)

    def __switchFormat(type):
        javaType = "com.aspose.ocr.Format"
        format = jpype.JClass(javaType)
        if type.name == "TEXT":
            return format.Text
        elif type.name == "DOCX":
            return format.Docx
        if type.name == "PDF":
                return format.Pdf
        if type.name == "XLSX":
                return format.Xlsx
        if type.name == "XML":
                return format.Xml
        if type.name == "JSON":
                return format.Json
        if type.name == "HTML":
                return format.Html
        if type.name == "EPUB":
                return format.Epub
        if type.name == "RTF":
                return format.Rtf
        if type.name == "PDF_NO_IMG":
                return format.PdfNoImg


    def convertInputTypeToJava(jType):
        return ModelsConverter.__switchInputType(jType)

    def __switchInputType(type):
        javaType = "com.aspose.ocr.InputType"
        inputType = jpype.JClass(javaType)
        if type.name == "SINGLE_IMAGE":
            return inputType.SingleImage
        elif type.name == "PDF":
            return inputType.PDF
        elif type.name == "TIFF":
            return inputType.TIFF
        elif type.name == "URL":
            return inputType.URL
        elif type.name == "DIRECTORY":
            return inputType.Directory
        elif type.name == "ZIP":
            return inputType.Zip
        elif type.name == "BASE64":
            return inputType.Base64



    def convertToJavaAreasMode(jType):
        return ModelsConverter.__switchAreasMode(jType)

    def __switchAreasMode(type):
        javaType = "com.aspose.ocr.DetectAreasMode"
        detectAreasMode = jpype.JClass(javaType)
        if type.name == "NONE":
            return detectAreasMode.NONE
        elif type.name == "DOCUMENT":
            return detectAreasMode.DOCUMENT
        elif type.name == "PHOTO":
            return detectAreasMode.PHOTO
        elif type.name == "COMBINE":
            return detectAreasMode.COMBINE
        elif type.name == "TABLE":
            return detectAreasMode.TABLE
        elif type.name == "CURVED_TEXT":
            return detectAreasMode.CURVED_TEXT
        elif type.name == "TEXT_IN_WILD":
            return detectAreasMode.TEXT_IN_WILD

    def convertToJavaLanguage(jType):
        return ModelsConverter.__switchLanguage(jType)

    def __switchLanguage(type):
        javaType = "com.aspose.ocr.Language"
        language = jpype.JClass(javaType)
        if type.name == "NONE":
            return language.Latin
        if type.name == "LATIN":
            return language.Latin
        if type.name == "CYRILLIC":
            return language.Cyrillic
        if type.name == "ENG":
            return language.Eng
        if type.name == "DEU":
            return language.Deu
        if type.name == "POR":
            return language.Por
        if type.name == "SPA":
            return language.Spa
        if type.name == "FRA":
            return language.Fra
        if type.name == "ITA":
            return language.Ita
        if type.name == "CZE":
            return language.Cze
        if type.name == "DAN":
            return language.Dan
        if type.name == "DUM":
            return language.Dum
        if type.name == "EST":
            return language.Est
        if type.name == "FIN":
            return language.Fin
        if type.name == "LAV":
            return language.Lav
        if type.name == "LIT":
            return language.Lit
        if type.name == "NOR":
            return language.Nor
        if type.name == "POL":
            return language.Pol
        if type.name == "RUM":
            return language.Rum
        if type.name == "SRP_HRV":
            return language.Srp_hrv
        if type.name == "SLK":
            return language.Slk
        if type.name == "SLV":
            return language.Slv
        if type.name == "SWE":
            return language.Swe
        if type.name == "CHI":
            return language.Chi
        if type.name == "BEL":
            return language.Bel
        if type.name == "BUL":
            return language.Bul
        if type.name == "KAZ":
            return language.Kaz
        if type.name == "RUS":
            return language.Rus
        if type.name == "SRP":
            return language.Srp
        if type.name == "UKR":
            return language.Ukr
        if type.name == "HIN":
            return language.Hin