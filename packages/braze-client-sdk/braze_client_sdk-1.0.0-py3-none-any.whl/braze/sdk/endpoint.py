from __future__ import annotations

import functools
from typing import (
    Optional,
    TYPE_CHECKING
)

if TYPE_CHECKING:  # pragma: no cover
    from . import Braze

__all__ = [
    "ContentBlocks",
    "Users"
]

from pydantic import validate_call

from .validators import *

from .shared import (
    api,
    prepare_request
)
from shared.types import DictT


class Endpoint:

    def __init__(self, braze: Braze):
        self.braze = braze


class ContentBlocks(Endpoint):

    @api.inject_call(endpoint="/content_blocks/list")
    @validate_call
    def ls(
            self,
            params: Optional[ContentBlocksListParams] = None,
            **kwargs
    ) -> DictT:
        """Documentation: https://www.braze.com/docs/api/endpoints/templates/content_blocks_templates/get_list_email_content_blocks/

        Parameters
        ----------
        params:
            - modified_after, Optional, String in ISO-8601 format
            - modified_before, Optional, String in ISO-8601 format
            - limit, Optional, Positive Number
            - offset, Optional, Positive Number

        Returns
        -------
        {
          "count": "integer",
          "content_blocks": [
            {
              "content_block_id": (string) the Content Block identifier,
              "name": (string) the name of the Content Block,
              "content_type": (string) the content type, html or text,
              "liquid_tag": (string) the Liquid tags,
              "inclusion_count" : (integer) the inclusion count,
              "created_at": (string) The time the Content Block was created in ISO 8601,
              "last_edited": (string) The time the Content Block was last edited in ISO 8601,
              "tags": (array) An array of tags formatted as strings,
            }
          ]
        }
        """
        return prepare_request(
            params=params,
            **kwargs
        )

    @api.inject_call(endpoint="/content_blocks/info")
    @validate_call
    def info(
            self,
            params: ContentBlocksInfoParams,
            **kwargs
    ) -> DictT:
        """Documentation: https://www.braze.com/docs/api/endpoints/templates/content_blocks_templates/get_see_email_content_blocks_information/

        Parameters
        ----------
        params:
            - content_block_id, Required, The Content Block identifier.
            - include_inclusion_data, Optional, When set to true, the API returns back the
              Message Variation API identifier of campaigns and Canvases where this Content Block is included,
              to be used in subsequent calls. The results exclude archived or deleted campaigns or Canvases.

        Returns
        -------
        {
          "content_block_id": (string) the Content Block identifier,
          "name": (string) the name of the Content Block,
          "content": (string) the content in the Content Block,
          "description": (string) the Content Block description,
          "content_type": (string) the content type, html or text,
          "tags": (array) An array of tags formatted as strings,
          "created_at": (string) The time the Content Block was created in ISO 8601,
          "last_edited": (string) The time the Content Block was last edited in ISO 8601,
          "inclusion_count" : (integer) the inclusion count,
          "inclusion_data": (array) the inclusion data,
          "message": "success",
        }
        """
        return prepare_request(
            params=params,
            **kwargs
        )

    @api.inject_call(endpoint="/content_blocks/create")
    def create(
            self,
            content: ContentBlocksCreateBody,
            **kwargs
    ) -> DictT:
        """Documentation: https://www.braze.com/docs/api/endpoints/templates/content_blocks_templates/post_create_email_content_block/

        Parameters
        ----------
        content: {
          "name": (required, string) Must be less than 100 characters,
          "description": (optional, string) The description of the Content Block. Must be less than 250 character,
          "content": (required, string) HTML or text content within Content Block,
          "state": (optional, string) Choose `active` or `draft`. Defaults to `active` if not specified,
          "tags": (optional, array of strings) Tags must already exist
        }

        Returns
        -------
        {
          "content_block_id": (string) Your newly generated block id,
          "liquid_tag": (string) The generated block tag from the Content Block name,
          "created_at": (string) The time the Content Block was created in ISO 8601,
          "message": "success"
        }
        """
        return prepare_request(
            json=content,
            method="POST",
            **kwargs
        )

    @api.inject_call(endpoint="/content_blocks/update")
    @validate_call
    def update(
            self,
            content: ContentBlocksUpdateBody,
            **kwargs
    ) -> DictT:
        """Documentation: https://www.braze.com/docs/api/endpoints/templates/content_blocks_templates/post_update_content_block/

        Parameters
        ----------
        content: {
          "content_block_id" : (required, string) Content Block's API identifier.
          "name": (optional, string) Must be less than 100 characters,
          "description": (optional, string) The description of the Content Block. Must be less than 250 character,
          "content": (optional, string) HTML or text content within Content Block,
          "state": (optional, string) Choose `active` or `draft`. Defaults to `active` if not specified,
          "tags": (optional, array of strings) Tags must already exist
        }

        Returns
        -------
        {
          "content_block_id": (string) Your newly generated block id,
          "liquid_tag": (string) The generated block tag from the Content Block name,
          "created_at": (string) The time the Content Block was created in ISO 8601,
          "message": "success"
        }
        """
        return prepare_request(
            json=content,
            method="POST",
            **kwargs
        )


class UsersAlias(Endpoint):

    @api.inject_call(endpoint="/users/alias/new")
    @validate_call
    def new(
            self,
            content: UsersAliasNewBody,
            **kwargs
    ) -> DictT:
        """Documentation: https://www.braze.com/docs/api/endpoints/user_data/post_user_alias/

        Parameters
        ----------
        content:
        {
          "user_aliases" : (required, array of new user alias object)
        }

        Returns
        -------
        {
          "aliases_processed": 1,
          "message": "success"
        }
        """
        return prepare_request(
            json=content,
            method="POST",
            **kwargs
        )

    @api.inject_call(endpoint="/users/alias/update")
    @validate_call
    def update(
            self,
            content: UsersAliasUpdateBody,
            **kwargs
    ):
        """Documentation: https://www.braze.com/docs/api/endpoints/user_data/post_users_alias_update/

        Parameters
        ----------
        content:
        {
          "alias_updates" : (required, array of update user alias object)
        }

        Returns
        -------
        Non-specified in their documentation
        """
        return prepare_request(
            json=content,
            method="POST",
            **kwargs
        )


class UsersExport(Endpoint):

    @api.inject_call(endpoint="/users/export/global_control_group")
    @validate_call
    def global_control_group(
            self,
            content: UsersExportGlobalControlGroupBody,
            **kwargs
    ) -> DictT:
        """Documentation: https://www.braze.com/docs/api/endpoints/export/user_data/post_users_global_control_group/

        Parameters
        ----------
        content:
        {
          "callback_endpoint" : (optional, string) endpoint to post a download URL to when the export is available,
          "fields_to_export" : (required, array of string) name of user data fields to export, for example, ['first_name', 'email', 'purchases'],
          "output_format" : (optional, string) When using your own S3 bucket, allows to specify file format as 'zip' or 'gzip'. Defaults to zip file format
        }

        Returns
        -------
        {
          "message": (required, string) the status of the export, returns 'success' when completed without errors,
          "object_prefix": (required, string) the filename prefix that will be used for the JSON file produced by this export, for example,'bb8e2a91-c4aa-478b-b3f2-a4ee91731ad1-1464728599',
          "url" : (optional, string) the URL where the segment export data can be downloaded if you do not have your own S3 credentials
        }
        """
        return prepare_request(
            json=content,
            method="POST",
            **kwargs
        )

    @api.inject_call(endpoint="/users/export/ids")
    @validate_call
    def ids(
            self,
            content: Optional[UsersExportIdsBody] = None,
            **kwargs
    ) -> DictT:
        """Documentation: https://www.braze.com/docs/api/endpoints/export/user_data/post_users_identifier/

        Parameters
        ----------
        content:
        {
          "external_ids": (optional, array of strings) External identifiers for users you wish to export,
          "user_aliases": (optional, array of user alias objects) user aliases for users to export,
          "device_id": (optional, string) Device identifier as returned by various SDK methods such as `getDeviceId`,
          "braze_id": (optional, string) Braze identifier for a particular user,
          "email_address": (optional, string) Email address of user,
          "phone": (optional, string) Phone number of user,
          "fields_to_export": (optional, array of strings) Name of user data fields to export. Defaults to all if not provided
        }

        Returns
        -------
        {
          "message": (required, string) the status of the export, returns 'success' when completed without errors,
          "users" : (array of object) the data for each of the exported users, may be empty if no users are found,
          "invalid_user_ids" : (optional, array of string) each of the identifiers provided in the request that did not correspond to a known user
        }
        """
        return prepare_request(
            json=content,
            method="POST",
            **kwargs
        )

    @api.inject_call(endpoint="/users/export/segment")
    @validate_call
    def segment(
            self,
            content: UsersExportSegmentBody,
            **kwargs
    ) -> DictT:
        """Documentation: https://www.braze.com/docs/api/endpoints/export/user_data/post_users_segment/

        Parameters
        ----------
        content: {
          "segment_id" : (required, string) identifier for the segment to be exported,
          "callback_endpoint" : (optional, string) endpoint to post a download URL when the export is available,
          "fields_to_export" : (required, array of string) name of user data fields to export, you may also export custom attributes. *Beginning April 2021, new accounts must specify specific fields to export.
          "output_format" : (optional, string) when using your own S3 bucket,  specifies file format as 'zip' or 'gzip'. Defaults to ZIP file format
        }

        Returns
        -------
        {
          "message": (required, string) the status of the export, returns 'success' when completed without errors,
          "object_prefix": (required, string) the filename prefix that will be used for the JSON file produced by this export, for example, 'bb8e2a91-c4aa-478b-b3f2-a4ee91731ad1-1464728599',
          "url" : (optional, string) the URL where the segment export data can be downloaded if you do not have your own S3 credentials
        }
        """
        return prepare_request(
            json=content,
            method="POST",
            **kwargs
        )


class Users(Endpoint):

    @functools.cached_property
    def alias(self):
        return UsersAlias(self.braze)

    @functools.cached_property
    def export(self):
        return UsersExport(self.braze)

    @api.inject_call(endpoint="/users/delete")
    @validate_call
    def delete(
            self,
            content: Optional[UsersDeleteBody] = None,
            **kwargs
    ) -> DictT:
        """Documentation: https://www.braze.com/docs/api/endpoints/user_data/post_user_delete/

        Parameters
        ----------
        content: {
          "external_ids" : (optional, array of string) External ids for the users to delete,
          "user_aliases" : (optional, array of user alias objects) User aliases for the users to delete,
          "braze_ids" : (optional, array of string) Braze user identifiers for the users to delete
        }

        Returns
        -------
        {
          "deleted" : (required, integer) number of user ids queued for deletion
        }
        """
        return prepare_request(
            json=content,
            method="POST",
            **kwargs
        )

    @api.inject_call(endpoint="/users/identify")
    @validate_call
    def identify(
            self,
            content: UsersIdentifyBody,
            **kwargs
    ) -> DictT:
        """Documentation: https://www.braze.com/docs/api/endpoints/user_data/post_user_identify/

        Parameters
        ----------
        content: {
          "aliases_to_identify" : (required, array of alias to identify objects),
          "merge_behavior": (optional, string) one of 'none' or 'merge' is expected
        }

        Returns
        -------
        {
          "aliases_processed": 1,
          "message": "success"
        }
        """
        return prepare_request(
            json=content,
            method="POST",
            **kwargs
        )

    @api.inject_call(endpoint="/users/merge")
    @validate_call
    def merge(
            self,
            content: UsersMergeBody,
            **kwargs
    ) -> DictT:
        """Documentation: https://www.braze.com/docs/api/endpoints/user_data/post_users_merge/

        Parameters
        ----------
        content: {
          "merge_updates" : (required, array of objects)
        }

        Returns
        -------
        {
          "message": "success"
        }
        """
        return prepare_request(
            json=content,
            method="POST",
            **kwargs
        )

    @api.inject_call(endpoint="/users/track")
    @validate_call
    def track(
            self,
            content: Optional[UsersTrackBody],
            **kwargs
    ) -> DictT:
        """Documentation: https://www.braze.com/docs/api/endpoints/user_data/post_user_track/

        Parameters
        ----------
        content: {
          "attributes" : (optional, array of attributes object),
          "events" : (optional, array of event object),
          "purchases" : (optional, array of purchase object),
        }

        Returns
        -------
        Successful message with non-fatal errors
        {
          "message" : "success",
          "errors" : [
            {
              <minor error message>
            }
          ]
        }

        Message with fatal errors
        {
          "message" : <fatal error message>,
          "errors" : [
            {
              <fatal error message>
            }
          ]
        }
        """
        return prepare_request(
            json=content,
            method="POST",
            **kwargs
        )
