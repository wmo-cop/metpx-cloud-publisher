# =================================================================
#
# Authors: Tom Kralidis <tomkralidis@gmail.com>
#
# Copyright (c) 2021 Tom Kralidis
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import logging
import os


class MetPXCloudPublisher:
    """core cloud data publisher"""

    def __init__(self, parent):
        """initialize"""

        self.type = os.environ.get('METPX_CLOUD_PUBLISHER_TYPE', None)

        self.container_name = os.environ.get(
            'METPX_CLOUD_PUBLISHER_CONTAINER_NAME', None)

        self.LOGGER = logging.getLogger(__name__)
        if None in [self.type, self.container_name]:
            raise EnvironmentError('environment variables not set')

    def dispatch(self, parent) -> bool:
        """
        sarracenia dispatcher

        :param parent: `sarra.sr_subscribe.sr_subscribe`

        :returns: `bool` of dispatch result
        """

        try:
            filepath = parent.msg.local_file
            parent.logger.debug('Filepath: {}'.format(filepath))
            identifier = filepath.replace(parent.currentDir, '').lstrip('/')

            if self.type == 'azure':
                self.publish_to_azure(identifier, filepath)

            return True

        except Exception as err:
            print("ERROR", err)
            parent.logger.warning(err)

            return False

    def publish_to_azure(self, parent, blob_identifier: str,
                         filepath: str) -> bool:
        """
        Azure blob file publisher

        :param blog_identifier: `str` of blob id
        :param filepath: `str` of local filepath to upload

        :returns: `bool` of dispatch result
        """

        from azure.core.exceptions import ResourceNotFoundError
        from azure.storage.blob import BlobServiceClient

        connection_string = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')

        try:
            blob_service_client = BlobServiceClient.from_connection_string(
                connection_string)
        except ValueError as err:
            self.LOGGER.error(err)
            return False

        blob_client = blob_service_client.get_blob_client(
            container=self.container_name,
            blob=blob_identifier)

        try:
            with open(filepath, 'rb') as data:
                result = blob_client.upload_blob(data)
                self.LOGGER.debug(result)
                self.LOGGER.info('published to {}'.format(blob_client.url))
                parent.msg.notice = blob_client.url
        except ResourceNotFoundError as err:
            self.LOGGER.error(err)
            return False

        return True

    def __repr__(self):
        return '<MetPXCloudPublisher>'


event = MetPXCloudPublisher(self)  # noqa
self.on_file = event.dispatch  # noqa
