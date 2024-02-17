#!/usr/bin/python

class GrabzItException(Exception):

        SUCCESS = 0
        PARAMETER_NO_URL = 100
        PARAMETER_INVALID_URL = 101
        PARAMETER_NON_EXISTANT_URL = 102
        PARAMETER_MISSING_APPLICATION_KEY = 103
        PARAMETER_UNRECOGNISED_APPLICATION_KEY = 104
        PARAMETER_MISSING_SIGNATURE = 105
        PARAMETER_INVALID_SIGNATURE = 106
        PARAMETER_INVALID_FORMAT = 107
        PARAMETER_INVALID_COUNTRY_CODE = 108
        PARAMETER_DUPLICATE_IDENTIFIER = 109
        PARAMETER_MATCHING_RECORD_NOT_FOUND = 110
        PARAMETER_INVALID_CALLBACK_URL = 111
        PARAMETER_NON_EXISTANT_CALLBACK_URL = 112
        PARAMETER_IMAGE_WIDTH_TOO_LARGE = 113
        PARAMETER_IMAGE_HEIGHT_TOO_LARGE = 114
        PARAMETER_BROWSER_WIDTH_TOO_LARGE = 115
        PARAMETER_BROWSER_HEIGHT_TOO_LARGE = 116
        PARAMETER_DELAY_TOO_LARGE = 117
        PARAMETER_INVALID_BACKGROUND = 118
        PARAMETER_INVALID_INCLUDE_LINKS = 119
        PARAMETER_INVALID_INCLUDE_OUTLINE = 120
        PARAMETER_INVALID_PAGE_SIZE = 121
        PARAMETER_INVALID_PAGE_ORIENTATION = 122
        PARAMETER_VERTICAL_MARGIN_TOO_LARGE = 123
        PARAMETER_HORIZONTAL_MARGIN_TOO_LARGE = 124
        PARAMETER_INVALID_COVER_URL = 125
        PARAMETER_NON_EXISTANT_COVER_URL = 126
        PARAMETER_MISSING_COOKIE_NAME = 127
        PARAMETER_MISSING_COOKIE_DOMAIN = 128
        PARAMETER_INVALID_COOKIE_NAME = 129
        PARAMETER_INVALID_COOKIE_DOMAIN = 130
        PARAMETER_INVALID_COOKIE_DELETE = 131
        PARAMETER_INVALID_COOKIE_HTTP = 132
        PARAMETER_INVALID_COOKIE_EXPIRY = 133
        PARAMETER_INVALID_CACHE_VALUE = 134
        PARAMETER_INVALID_DOWNLOAD_VALUE = 135
        PARAMETER_INVALID_SUPPRESS_VALUE = 136
        PARAMETER_MISSING_WATERMARK_IDENTIFIER = 137
        PARAMETER_INVALID_WATERMARK_IDENTIFIER = 138
        PARAMETER_INVALID_WATERMARK_XPOS = 139
        PARAMETER_INVALID_WATERMARK_YPOS = 140
        PARAMETER_MISSING_WATERMARK_FORMAT = 141
        PARAMETER_WATERMARK_TOO_LARGE = 142
        PARAMETER_MISSING_PARAMETERS = 143
        PARAMETER_QUALITY_TOO_LARGE = 144
        PARAMETER_QUALITY_TOO_SMALL = 145
        PARAMETER_REPEAT_TOO_SMALL = 149
        PARAMETER_INVALID_REVERSE = 150
        PARAMETER_FPS_TOO_LARGE = 151
        PARAMETER_FPS_TOO_SMALL = 152
        PARAMETER_SPEED_TOO_FAST = 153
        PARAMETER_SPEED_TOO_SLOW = 154
        PARAMETER_INVALID_ANIMATION_COMBINATION = 155
        PARAMETER_START_TOO_SMALL = 156
        PARAMETER_DURATION_TOO_SMALL = 157
        PARAMETER_NO_HTML = 163
        PARAMETER_INVALID_TARGET_VALUE = 165
        PARAMETER_INVALID_HIDE_VALUE = 166     
        PARAMETER_INVALID_INCLUDE_IMAGES = 167       
        PARAMETER_INVALID_EXPORT_URL = 168
        PARAMETER_INVALID_WAIT_FOR_VALUE = 169
        PARAMETER_INVALID_TRANSPARENT_VALUE = 170
        PARAMETER_INVALID_ENCRYPTION_KEY = 171
        PARAMETER_INVALID_NO_ADS = 172
        PARAMETER_INVALID_PROXY = 173
        PARAMETER_INVALID_NO_NOTIFY = 174
        PARAMETER_INVALID_HD = 176
        PARAMETER_INVALID_MEDIA_TYPE = 177
        PARAMETER_INVALID_PASSWORD = 178
        PARAMETER_INVALID_MERGE = 179
        PARAMETER_INVALID_CLICK_VALUE = 180
        NETWORK_SERVER_OFFLINE = 200
        NETWORK_GENERAL_ERROR = 201
        NETWORK_DDOS_ATTACK = 202
        RENDERING_ERROR = 300
        RENDERING_MISSING_SCREENSHOT = 301
        GENERIC_ERROR = 400
        UPGRADE_REQUIRED = 500
        FILE_SAVE_ERROR = 600
        FILE_NON_EXISTANT_PATH = 601

        def __init__(self, message, code):
                Exception.__init__(self, message)
                self.Code = code