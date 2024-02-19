import ipih

from pih import A
from RecognizeService.const import SD

# version 0.8
SC = A.CT_SC

if A.U.for_service(
    SD,
    [
        "fuzzywuzzy",
        "pyzbar",
        "opencv-python",
        "pytesseract",
        "deskew",
        "rembg==2.0.53",
        "mrz",
        "ocrmypdf",
        "PyPDF2",
        "reportlab",
        "python-Levenshtein",
    ],
):
    from typing import Any
    from pih.tools import ParameterList, ne, e, nn, j, js, while_excepted
    from pih.collections import (
        OGRN,
        Result,
        BarcodeInformation,
        ChillerIndicationsValue,
        PolibaseDocument,
        PolibaseDocumentDescription,
    )
    from MobileHelperService.api import MobileOutput
    from MobileHelperService.client import Client as MIO
    from MobileHelperService.tools import Logger
    from RecognizeService.api import (
        RecognizeApi as Api,
        RecognizeResult,
        #MedicalDirectionDocumentRecognizeResult,
        RecognizeConfig,
        PolibaseDocumentRecognizeResult,
        #PersonalDocumentRecognizeResult,
        #PERSONAL_DOCUMENT_TYPES,
        PageCorrections,
    )
    import ocrmypdf
    from PIL import Image
    from io import BytesIO
    from datetime import datetime
    from PyPDF2 import PdfWriter, PdfReader, PageObject
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.colors import black, white
    import time
    import shutil
    from DocsService.tools import Converter
    import os

    TEST_PATH: str = A.PTH.SCAN_TEST.VALUE

    class SETTINGS:
        recognize_document: bool = True
        log_level: int = 0

    class TEST_SETTINGS:
        recognize_document: bool = False
        recognize_seven_segments_display: bool = False
        file_list: list[str] = []
        # [file for file in listdir(TEST_PATH) if isfile(A.PTH.join(TEST_PATH, file))]
        file_list.reverse()
        input_file_list: list[str] = []
        # ["diag167.pdf"]
        specific_pages_of_document: list[int] | None = []
        document_type: list[A.CT_DT] | None = []
        log_level: int = 0
        ocr: bool = True

    logger_output: MobileOutput = MIO.create_output(
        A.D.get(A.CT_ME_WH.GROUP.DOCUMENTS_WORK_STACK)
    )
    test_logger_output: MobileOutput = MIO.create_output(
        A.D.get(A.CT_ME_WH.GROUP.DOCUMENTS_WORK_STACK_TEST)
    )
    logger: Logger = Logger(logger_output, TEST_SETTINGS.log_level)
    test_logger: Logger = Logger(
        test_logger_output, A.S.get(A.CT_S.CHILLER_RECOGNIZE_LOG_LEVEL)
    )

    def get_logger_output(test: bool) -> MobileOutput:
        return test_logger_output if test else logger_output

    def get_logger(test: bool) -> Logger:
        return test_logger if test else logger

    recognize_api: Api = Api(test_logger)

    def recognize_display(indications_value: ChillerIndicationsValue) -> None:
        recognize_api.recognize_display(indications_value)

    def service_call_handler(sc: SC, parameter_list: ParameterList) -> Any:
        if sc == SC.register_chiller_indications_value:
            indications_value: ChillerIndicationsValue = parameter_list.next(
                ChillerIndicationsValue()
            )
            if e(indications_value.temperature):
                recognize_display(indications_value)
            return indications_value
        if sc == SC.recognize_document:
            path: str = parameter_list.next()
            document_type: A.CT_DT | None = A.D.get_by_value(
                A.CT_DT, parameter_list.next()
            )
            return_result: bool = parameter_list.next()
            result: bool | PolibaseDocument | None = recognize_document(
                path,
                document_type=document_type,
                log_level=2,
                force=True,
                return_result=return_result,
            )
            if return_result:
                return A.R.pack(A.CT_FCA.VALUE, result)
            return True
        if sc == SC.document_type_exists:
            return recognize_document(
                parameter_list.next(),
                A.D.get(A.CT_DT, parameter_list.next(), parameter_list.next()),
            )
        if sc == SC.get_barcode_list_information:
            source_file_path: str = parameter_list.next()
            _: bool = parameter_list.next()
            log_level: int = parameter_list.next()
            get_logger(True).level = log_level
            source_file_extension: str = A.PTH.get_extension(source_file_path)
            pdf_format_detected: bool = source_file_extension == A.CT_F_E.PDF
            image_format_detected: bool = source_file_extension in [
                A.CT_F_E.JPEG,
                A.CT_F_E.JPG,
            ]
            page_image_list: list[Image.Image] | None = None
            if pdf_format_detected or image_format_detected:
                while True:
                    try:
                        page_image_list = (
                            Converter.pdf_to_pages_as_image_list(source_file_path)
                            if pdf_format_detected
                            else [Image.open(source_file_path)]
                        )
                        break
                    except Exception as _:
                        time.sleep(2)
                result: list[list[BarcodeInformation]] = []
                if len(page_image_list) > 0:
                    for page_image in page_image_list:
                        barcode_information_list: list[
                            BarcodeInformation
                        ] = recognize_api.read_barcode_information(page_image)
                        result.append(barcode_information_list)
                return A.R.pack(A.CT_FCA.VALUE_LIST, result)
        return None

    def recognize_document(
        file_path: str,
        document_type: A.CT_DT | None = None,
        log_level: int | None = None,
        force: bool = False,
        return_result: bool = False,
    ) -> bool | PolibaseDocument | None:
        log_level = log_level or TEST_SETTINGS.log_level
        get_logger(True).level = log_level
        #
        file_name: str = A.PTH.get_file_name(file_path).lower()
        file_extension: str = A.PTH.get_extension(file_path)
        #
        pdf_format_detected: bool = file_extension == A.CT_F_E.PDF
        image_format_detected: bool = file_extension in [A.CT_F_E.JPEG, A.CT_F_E.JPG]
        #
        if pdf_format_detected or image_format_detected:
            source_file_directory: str = A.PTH.get_file_directory(file_path)
            scanned_file_detected: bool = source_file_directory == A.PTH.path(
                A.PTH.SCAN_RESULT.get_path(A.CT_DT.MEDICAL_DIRECTION)
            )
            test_scanned_file_detected: bool = source_file_directory == A.PTH.path(
                TEST_PATH
            )
            if (
                nn(document_type)
                or (TEST_SETTINGS.recognize_document and test_scanned_file_detected)
                or (SETTINGS.recognize_document and scanned_file_detected)
                or force
            ):
                page_list: list[Image.Image] | None = None
                while True:
                    try:
                        page_list = (
                            Converter.pdf_to_pages_as_image_list(file_path)
                            if pdf_format_detected
                            else [Image.open(file_path)]
                        )
                        break
                    except Exception:
                        time.sleep(2)
                if len(page_list) > 0:
                    page_image: Image.Image = page_list[0]
                    if TEST_SETTINGS.log_level >= 1:
                        scan_source_title: str | None = None
                        if scanned_file_detected:
                            for scan_source_item in A.CT_SCN.Sources:
                                scan_source_item_value: tuple[str, str] = A.D.get(
                                    scan_source_item
                                )
                                if file_name.startswith(scan_source_item_value[0]):
                                    scan_source_title = scan_source_item_value[1]
                                    break
                        if test_scanned_file_detected:
                            scan_source_title = A.D.get(A.CT_SCN.Sources.TEST)[1]
                        if ne(scan_source_title):
                            get_logger(test_scanned_file_detected).write_image(
                                f"Входящий документ: {A.PTH.add_extension(file_name, file_extension)} {get_logger_output(test_scanned_file_detected).bold(f'({scan_source_title})')}. Первая страница",
                                page_image,
                            )
                    page_recognizer: Api | None = None
                    result: RecognizeResult | None = None
                    result_map: dict[int, RecognizeResult] = {}
                    polibase_document_recognize_result_map: dict[
                        int, PolibaseDocumentRecognizeResult
                    ] = {}
                    if TEST_SETTINGS.recognize_document and ne(
                        TEST_SETTINGS.specific_pages_of_document
                    ):
                        for page_index in range(len(page_list)):
                            if (
                                page_index
                                not in TEST_SETTINGS.specific_pages_of_document
                            ):
                                result_map[page_index] = RecognizeResult()
                    if document_type == A.CT_DT.POLIBASE and (
                        not TEST_SETTINGS.recognize_document
                        or e(TEST_SETTINGS.document_type)
                        or A.CT_DT.POLIBASE in TEST_SETTINGS.document_type
                    ):
                        for page_index, page in enumerate(page_list):
                            if page_index in result_map:
                                continue
                            page_recognizer = Api(
                                get_logger(test_scanned_file_detected)
                            )
                            page_recognizer.recognize_image(
                                page,
                                RecognizeConfig(
                                    True,
                                    False,
                                    False,
                                    return_only_document_type=True,
                                ),
                            )
                            result = page_recognizer.result
                            if ne(result):
                                polibase_scanned_document: PolibaseDocument | None = (
                                    None
                                )
                                if ne(document_type) and ne(result.type):
                                    return result.type == document_type
                                result_map[page_index] = result
                                polibase_document_recognize_result: PolibaseDocumentRecognizeResult | None = (
                                    page_recognizer.polibase_document_result
                                )
                                if ne(polibase_document_recognize_result):
                                    polibase_document_recognize_result_map[
                                        page_index
                                    ] = polibase_document_recognize_result
                                    polibase_document_description: PolibaseDocumentDescription = (
                                        polibase_document_recognize_result.type.value
                                    )
                                    for medical_direction_index in range(
                                        polibase_document_description.page_count - 1
                                    ):
                                        result_map[
                                            page_index + medical_direction_index + 1
                                        ] = result
                                        polibase_document_recognize_result_map[
                                            page_index + medical_direction_index + 1
                                        ] = polibase_document_recognize_result
                                    if not test_scanned_file_detected and ne(
                                        polibase_document_recognize_result
                                    ):
                                        polibase_scanned_document = PolibaseDocument(
                                            file_path,
                                            result.polibase_person_pin,
                                            polibase_document_recognize_result.type.name,
                                        )
                                if return_result:
                                    return polibase_scanned_document
                            else:
                                if return_result:
                                    return None
                    medical_direction_document_result_map: dict[
                        int, MedicalDirectionDocumentRecognizeResult
                    ] = {}
                    if document_type == A.CT_DT.MEDICAL_DIRECTION and (
                        not TEST_SETTINGS.recognize_document
                        or e(TEST_SETTINGS.document_type)
                        or A.CT_DT.MEDICAL_DIRECTION in TEST_SETTINGS.document_type
                    ):
                        for page_index, page in enumerate(page_list):
                            if page_index in result_map:
                                continue
                            page_recognizer = Api(
                                get_logger(test_scanned_file_detected)
                            )
                            page_recognizer.recognize_image(
                                page,
                                RecognizeConfig(False, True, False, False, False),
                            )
                            result = page_recognizer.result
                            if ne(result):
                                #check?
                                # if ne(document_type) and ne(result.type):
                                #    return result.type == document_type
                                result_map[page_index] = result
                                medical_direction_document_result_map[
                                    page_index
                                ] = (
                                    page_recognizer.medical_direction_document_holder.result
                                )
                    personal_document_recognize_result_map: dict[
                        int, PersonalDocumentRecognizeResult
                    ] = {}
                    """
                    if document_type == A.CT_DT.PERSONAL and (
                        not TEST_SETTINGS.recognize_document
                        or e(TEST_SETTINGS.document_type)
                        or A.CT_DT.PERSONAL in TEST_SETTINGS.document_type
                    ):
                        for page_index, page in enumerate(page_list):
                            if page_index in result_map:
                                continue
                            page_recognizer = Api(
                                get_logger(test_scanned_file_detected)
                            )
                            passport_first_page_found: bool = ne(
                                list(
                                    filter(
                                        lambda item: item.type
                                        == PERSONAL_DOCUMENT_TYPES.PASSPORT
                                        and item.page_index == 0,
                                        personal_document_recognize_result_map.values(),
                                    )
                                )
                            )
                            page_recognizer.recognize_image(
                                page,
                                RecognizeConfig(
                                    False,
                                    False,
                                    True,
                                    passport_first_page_found=passport_first_page_found,
                                    return_only_document_type=False,
                                ),
                            )
                            personal_document_recognize_result: PersonalDocumentRecognizeResult | None = (
                                page_recognizer.personal_document_result
                            )
                            if ne(personal_document_recognize_result):
                                personal_document_recognize_result_map[
                                    page_index
                                ] = personal_document_recognize_result
                            result = page_recognizer.result
                            if ne(result):
                                if ne(document_type) and ne(result.type):
                                    return result.type == document_type
                                result_map[page_index] = result
                    """
                    if ne(medical_direction_document_result_map):
                        result_with_person_name: RecognizeResult | None = None
                        personal_document_recognize_result: PersonalDocumentRecognizeResult | None = (
                            None
                        )
                        if ne(result_map):
                            for page_index in result_map:
                                result_with_person_name = result_map[page_index]
                                if ne(result_with_person_name.person_name) and ne(
                                    result_with_person_name.polibase_person_pin
                                ):
                                    break
                            if ne(personal_document_recognize_result_map):
                                for (
                                    page_index
                                ) in personal_document_recognize_result_map:
                                    personal_document_recognize_result_item: PersonalDocumentRecognizeResult = personal_document_recognize_result_map[
                                        page_index
                                    ]
                                    if (
                                        personal_document_recognize_result_item.type
                                        == PERSONAL_DOCUMENT_TYPES.PASSPORT
                                    ):
                                        personal_document_recognize_result = (
                                            personal_document_recognize_result_item
                                        )
                                        break
                            today: datetime = A.D.today(as_datetime=True)
                            year_string: str = str(today.year)
                            result_path: str = A.PTH.join(A.PTH.OMS.VALUE, "Done")
                            result_path = A.PTH.join(result_path, year_string)
                            A.PTH.make_directory_if_not_exists(result_path)
                            result_path = A.PTH.join(
                                result_path,
                                A.D.datetime_to_string(
                                    today, A.CT.YEARLESS_DATE_FORMAT
                                ),
                            )
                            A.PTH.make_directory_if_not_exists(result_path)
                            has_person_name: bool = ne(result_with_person_name) and ne(
                                result_with_person_name.person_name
                            )
                            ###
                            medical_direction_type_string: str = "неизвестно"
                            person_name_string: str = "ФИО неизвестна"
                            medical_direction_type_string = j(
                                A.D.map(
                                    lambda item: item.type.alias,
                                    A.D.filter(
                                        lambda item: ne(item.type),
                                        list(medical_direction_document_result_map.values()),
                                    ),
                                ),
                                ", ",
                            )
                            ###
                            if has_person_name:
                                name_list: list[str] = A.D.split_with_not_empty_items(
                                    result_with_person_name.person_name, " "
                                )
                                person_name_string = js(
                                    (
                                        A.D.capitalize(name_list[0].lower()),
                                        j(
                                            A.D.map(
                                                lambda item: str(item[0]).upper(),
                                                name_list[1:],
                                            ),
                                            ". ",
                                        ),
                                    )
                                )
                            result_path = A.PTH.join(
                                result_path,
                                A.PTH.add_extension(
                                    f"{person_name_string}. Направление {medical_direction_type_string}",
                                    file_extension,
                                ),
                            )
                            preresult_path: str = A.PTH.join(
                                A.PTH.APP_DATA.OCR_RESULT_FOLDER,
                                A.PTH.add_extension(A.D.uuid(), A.CT_F_E.PDF),
                            )
                            ocr_pdf_writer = PdfWriter()
                            source_pdf_reader = PdfReader(file_path, "rb")

                            def rotate_page(
                                result: RecognizeResult, page: PageObject
                            ) -> None:
                                if page_index in result_map:
                                    page_correction: PageCorrections | None = (
                                        result.page_correction
                                    )
                                    if (
                                        page_correction
                                        == PageCorrections.ROTATE_90_COUNTER
                                    ):
                                        page.rotate(-90)
                                    if page_correction == PageCorrections.ROTATE_90:
                                        page.rotate(90)
                                    if page_correction == PageCorrections.ROTATE_180:
                                        page.rotate(180)

                            for page_index in result_map:
                                result = result_map[page_index]
                                if (
                                    ne(result.type)
                                    and result.type == A.CT_DT.MEDICAL_DIRECTION
                                ):
                                    rotate_page(
                                        result, source_pdf_reader.pages[page_index]
                                    )
                                    ocr_pdf_writer.add_page(
                                        source_pdf_reader.pages[page_index]
                                    )
                            for page_index in result_map:
                                result = result_map[page_index]
                                """
                                if ne(result.type) and result.type == A.CT_DT.PERSONAL:
                                    rotate_page(
                                        result, source_pdf_reader.pages[page_index]
                                    )
                                    ocr_pdf_writer.add_page(
                                        source_pdf_reader.pages[page_index]
                                    )
                                """
                                ocr_pdf_file_path: str = A.PTH.join(
                                    A.PTH.APP_DATA.OCR_RESULT_FOLDER,
                                    A.PTH.add_extension(A.D.uuid(), A.CT_F_E.PDF),
                                )
                            with open(
                                ocr_pdf_file_path
                                if TEST_SETTINGS.ocr
                                else preresult_path,
                                "wb",
                            ) as file:
                                ocr_pdf_writer.write(file)
                            sidecar_path: str = A.PTH.join(
                                A.PTH.APP_DATA.OCR_RESULT_FOLDER,
                                A.PTH.add_extension(A.D.uuid(), A.CT_F_E.TXT),
                            )
                            ocrmypdf.ocr(
                                ocr_pdf_file_path,
                                preresult_path,
                                language=["rus"],
                                deskew=True,
                                clean=True,
                                clean_final=True,
                                sidecar=sidecar_path,
                            )
                            #
                            text_contents: str | None = None
                            with open(sidecar_path, "r", encoding="UTF-8") as file:
                                text_contents = file.readlines()
                            try:
                                result_pdf_file = PdfReader(open(preresult_path, "rb"))
                                packet = BytesIO()
                                pdfmetrics.registerFont(
                                    TTFont(
                                        A.CT_FNT.FOR_PDF,
                                        A.PTH_FNT.get(A.CT_FNT.FOR_PDF),
                                        "UTF-8",
                                    )
                                )
                                canvas = Canvas(packet, pagesize=A4)
                                textobject = canvas.beginText(20, 200)
                                textobject.setFont(A.CT_FNT.FOR_PDF, 11)
                                result_text: str = (
                                    f"Пациент: {result_with_person_name.person_name}\n"
                                )
                                if ne(personal_document_recognize_result):
                                    result_text += "Паспорт:"
                                    result_text += f"   Серия и номер: {personal_document_recognize_result.data.number}\n"
                                    result_text += f"   Когда выдан: {A.D.datetime_to_string(personal_document_recognize_result.data.issue_date, A.CT.DATE_FORMAT)}\n"
                                    fms_unit_result: Result[
                                        str | None
                                    ] = A.R_DS.fms_unit_name(
                                        personal_document_recognize_result.data.fms_unit_code
                                    )
                                    if not A.R.is_empty(fms_unit_result):
                                        result_text += f"   Кем выдан: {fms_unit_result.data.lower()}\n"
                                has_medical_direction_document = ne(
                                    medical_direction_document_result_map
                                )
                                if has_medical_direction_document:
                                    for (
                                        medical_direction_index,
                                        page_index,
                                    ) in enumerate(
                                        medical_direction_document_result_map
                                    ):
                                        medical_direction_result: MedicalDirectionDocumentRecognizeResult = medical_direction_document_result_map[
                                            page_index
                                        ]
                                        result_text += f"Направление {medical_direction_index + 1}: {medical_direction_result.number}\n"
                                        ogrn: OGRN | None = A.R_DS.ogrn(
                                            medical_direction_result.ogrn_number
                                        ).data
                                        if ne(ogrn):
                                            result_text += (
                                                f"   Мед. учереждение: {ogrn.name}\n"
                                            )
                                        result_text += f"   Тип: {medical_direction_result.type_code} ({medical_direction_result.type.alias})\n"
                                        result_text += f"   Дата: {A.D.datetime_to_string(medical_direction_result.date, A.CT.DATE_FORMAT)}\n"
                                    result_text += f"Дата рождения: {A.D.datetime_to_string(medical_direction_result.person_birthday, A.CT.DATE_FORMAT)}\n"
                                    result_text += f"Номер страхового полюса: {medical_direction_result.person_ensurence_number}\n"
                                    result_text += f"Страхователь: {medical_direction_result.person_ensurence_agent}\n"
                                    if TEST_SETTINGS.log_level >= 1:
                                        get_logger(
                                            test_scanned_file_detected
                                        ).write_line(result_text)
                                    width, _ = A4
                                    canvas.setFillColor(black)
                                    canvas.rect(
                                        20, 10, width - 40, 250, stroke=True, fill=True
                                    )
                                    canvas.setFillColor(white)
                                    for line in result_text.splitlines(False):
                                        textobject.textLine(line.rstrip())
                                    canvas.drawText(textobject)
                                canvas.save()
                                packet.seek(0)
                                modificated_pdf_file = PdfReader(packet)
                                result_output = PdfWriter()
                                for page_index, page in enumerate(
                                    result_pdf_file.pages
                                ):
                                    if page_index == 0:
                                        page.merge_page(
                                            modificated_pdf_file.pages[page_index]
                                        )
                                    result_output.add_page(page)
                                for (
                                    page_index
                                ) in polibase_document_recognize_result_map:
                                    polibase_document_recognize_result: PolibaseDocumentRecognizeResult = polibase_document_recognize_result_map[
                                        page_index
                                    ]
                                    result_output.add_page(
                                        source_pdf_reader.pages[page_index]
                                    )
                                result_output_stream = open(result_path, "wb")
                                result_output.write(result_output_stream)
                                result_output_stream.close()
                                if test_scanned_file_detected:
                                    os.remove(file_path)
                            except Exception as error:
                                shutil.move(preresult_path, result_path)
                                get_logger(test_scanned_file_detected).error(
                                    f"Ошибка аннотации документа {error}"
                                )
                        else:
                            pass
                else:
                    pass
            else:
                pass
        else:
            pass

    def service_starts_handler() -> None:
        A.SRV_A.subscribe_on(
            SC.register_chiller_indications_value, A.CT_SubT.ON_PARAMETERS
        )
        if TEST_SETTINGS.recognize_document and ne(TEST_SETTINGS.input_file_list):
            for file_name in TEST_SETTINGS.input_file_list:
                recognize_document(A.PTH.join(A.PTH.SCAN_TEST.VALUE, file_name))
        if TEST_SETTINGS.recognize_seven_segments_display:
            recognize_display(ChillerIndicationsValue())

    A.SRV_A.serve(SD, service_call_handler, service_starts_handler)
