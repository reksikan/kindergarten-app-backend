from typing import List

from fastapi import APIRouter, Request, HTTPException, UploadFile
from starlette.responses import FileResponse

from .base import BaseRouter, add_route
from src.api.security import SecurityMiddleware
from src.schemas.receipts import ReceiptSchema, CreateReceiptSchema, SBPPaymentSchema
from src.enums.permissions import PermissionAccess, PermissionAction
from src.enums.receipt import ReceiptStatus
from src.db.models.account import Account
from src.db.models.kindergarten import Kindergarten
from ..enums.file_extensions import FileExtensions


class ReceiptRouter(BaseRouter):
    _router = APIRouter(prefix='/receipts', tags=['receipts'])
    endpoints = []

    @add_route(
        endpoints,
        '/',
        methods=['GET'],
        response_model=List[ReceiptSchema],
        dependencies=[SecurityMiddleware(
            parents_available=True,
            staff_available=True,
            admin_available=True,
            access_type=PermissionAccess.READ,
            access_action=PermissionAction.PAYMENTS,
        )]
    )
    async def receipts_list(self, request: Request):
        account: Account = request.state.account
        if account.staff:
            return await self._db_manager.receipts.receipts_by_staff_id(account.id)
        return await self._db_manager.receipts.receipts_by_parent_id(account.id)

    @add_route(
        endpoints,
        '/{receipt_id}/payment',
        methods=['POST'],
        response_model=SBPPaymentSchema,
        dependencies=[SecurityMiddleware(
            parents_available=True
        )],
    )
    async def create_sbp_payment(self, request: Request, receipt_id: int):
        account: Account = request.state.account
        receipt = await self._db_manager.receipts.get_receipt_by_id(receipt_id)

        for child_parent in receipt.child.child_parent:
            if child_parent.parent_id == account.parent.id:
                break
        else:
            raise HTTPException(status_code=404)

        if receipt.status is ReceiptStatus.PAID:
            raise HTTPException(status_code=422, detail='Already paid')

        sbp_payment = receipt.sbp_payment
        if sbp_payment is None:
            link = self._service_manager.sbp_client.create_payment_link(receipt.amount)
            sbp_payment = await self._db_manager.sbp_payments.create_payment(receipt_id, link)

        return sbp_payment

    @add_route(
        endpoints,
        '/{receipt_id}/payment',
        methods=['GET'],
        response_model=ReceiptSchema,
        dependencies=[SecurityMiddleware(
            parents_available=True
        )],
    )
    async def check_sbp_payment(self, request: Request, receipt_id: int):
        account: Account = request.state.account
        receipt = await self._db_manager.receipts.get_receipt_by_id(receipt_id)

        for child_parent in receipt.child.child_parent:
            if child_parent.parent_id == account.parent.id:
                break
        else:
            raise HTTPException(status_code=404)

        if receipt.status is ReceiptStatus.PAID:
            return receipt

        sbp_payment = receipt.sbp_payment
        if sbp_payment is None:
            raise HTTPException(status_code=404)

        if self._service_manager.sbp_client.check_payment_link(sbp_payment.link):
            receipt = await self._db_manager.receipts.confirm_receipt(receipt)

        return receipt

    @add_route(
        endpoints,
        '/{receipt_id}',
        methods=['GET'],
        response_model=ReceiptSchema,
        dependencies=[SecurityMiddleware(
            parents_available=True,
            staff_available=True,
            admin_available=True,
            access_type=PermissionAccess.READ,
            access_action=PermissionAction.PAYMENTS,
        )]
    )
    async def receipt_by_id(self, receipt_id: int, request: Request):
        account: Account = request.state.account

        receipt = await self._db_manager.receipts.get_receipt_by_id(receipt_id)
        if not receipt:
            raise HTTPException(status_code=404)

        if account.staff:
            for staff in receipt.kindergarten.staff:
                if staff.id == account.staff.id:
                    return receipt
            raise HTTPException(status_code=404)

        for child_parent in receipt.child.child_parent:
            if child_parent.parent_id == account.parent.id:
                return receipt
        raise HTTPException(status_code=404)

    @add_route(
        endpoints,
        '/{receipt_id}/export',
        methods=['GET'],
        response_class=FileResponse,
        dependencies=[SecurityMiddleware(
            parents_available=True,
            staff_available=True,
            admin_available=True,
            access_type=PermissionAccess.READ,
            access_action=PermissionAction.PAYMENTS,
        )]
    )
    async def export_receipt_by_id(
        self,
        receipt_id: int,
        request: Request,
        file_ext: FileExtensions = FileExtensions.PDF.value,
    ):
        account: Account = request.state.account

        receipt = await self._db_manager.receipts.get_receipt_by_id(receipt_id)
        if not receipt:
            raise HTTPException(status_code=404)

        if account.staff:
            for staff in receipt.kindergarten.staff:
                if staff.id == account.staff.id:
                    return FileResponse(self._service_manager.dock_generator.receipt_to_file(receipt, file_ext))
            raise HTTPException(status_code=404)

        for child_parent in receipt.child.child_parent:
            if child_parent.parent_id == account.parent.id:
                return FileResponse(self._service_manager.dock_generator.receipt_to_file(receipt, file_ext))
        raise HTTPException(status_code=404)

    @add_route(
        endpoints,
        '/',
        methods=['POST'],
        response_model=ReceiptSchema,
        dependencies=[SecurityMiddleware(
            staff_available=True,
            admin_available=True,
            access_type=PermissionAccess.EDIT,
            access_action=PermissionAction.PAYMENTS,
        )]
    )
    async def receipts_create(self, request: Request, body: CreateReceiptSchema):
        account: Account = request.state.account
        kindergarten: Kindergarten = account.staff.kindergarten
        child = await self._db_manager.children.get_by_id(body.child_id)

        if not child or not child.current_group.kindergaret_id == kindergarten.id:
            raise HTTPException(status_code=422)

        return await self._db_manager.receipts.create_receipt(
            kindergarten=kindergarten,
            child=child,
            type_=body.type,
            amount=body.amount
        )

    @add_route(
        endpoints,
        '/import',
        methods=['POST'],
        response_model=ReceiptSchema,
        dependencies=[SecurityMiddleware(
            staff_available=True,
            admin_available=True,
            access_type=PermissionAccess.EDIT,
            access_action=PermissionAction.PAYMENTS,
        )]
    )
    async def import_receipt(self, request: Request, file: UploadFile):
        receipt_schema = self._service_manager.dock_generator.parse_file_to_receipt(file)
        account: Account = request.state.account
        kindergarten: Kindergarten = account.staff.kindergarten
        child = await self._db_manager.children.get_by_id(receipt_schema.child_id)

        if not child or not child.current_group.kindergaret_id == kindergarten.id:
            raise HTTPException(status_code=422)

        return await self._db_manager.receipts.create_receipt(
            kindergarten=kindergarten,
            child=child,
            type_=receipt_schema.type,
            amount=receipt_schema.amount
        )

    @add_route(
        endpoints,
        '/{receipt_id}',
        methods=['POST'],
        dependencies=[SecurityMiddleware(
            staff_available=True,
            admin_available=True,
            access_type=PermissionAccess.EDIT,
            access_action=PermissionAction.PAYMENTS,
        )]
    )
    async def confirm_receipt_payment(self, request: Request, receipt_id: int):
        account: Account = request.state.account
        receipt = await self._db_manager.receipts.get_receipt_by_id(receipt_id)
        if not receipt or not account.staff.kindergarten_id == receipt.kindergarten_id:
            raise HTTPException(status_code=404)
        await self._db_manager.receipts.confirm_receipt(receipt)
