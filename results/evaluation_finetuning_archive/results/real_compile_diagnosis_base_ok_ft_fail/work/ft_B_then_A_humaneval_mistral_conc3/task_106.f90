program main
implicit none
integer, dimension(:), allocatable :: a
integer :: n
n = 5
a = f(n)
print *, a
contains
function f(n) result(res)
implicit none
integer, intent(in) :: n
integer, dimension(n) :: res
integer :: i
do i = 1, n
    if (mod(i, 2) == 0) then
        res(i) = factorial(i)
    else
        res(i) = sum(1:i)
    end if
end do
end function f
function factorial(n) result(res)
implicit none
integer, intent(in) :: n
integer :: res
res = 1
do i = 2, n
    res = res * i
end do
end function factorial
end program main