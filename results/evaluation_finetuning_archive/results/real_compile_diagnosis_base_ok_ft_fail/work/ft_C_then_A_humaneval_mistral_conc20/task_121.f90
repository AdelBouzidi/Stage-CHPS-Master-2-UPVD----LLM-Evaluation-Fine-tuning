program solution
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: lst_len
  integer, allocatable :: lst(:)
  integer :: result

  ! Hardcoded input as per example
  lst_len = 4
  allocate(lst(lst_len))
  lst = [5, 8, 7, 1]

  result = solution(lst_len, lst)

  print *, result

contains

  integer function solution(lst_len, lst)
    integer, intent(in) :: lst_len
    integer, intent(in) :: lst(:)
    integer :: i
    integer :: sum_val
    sum_val = 0
    do i = 2, lst_len, 2
      if (mod(lst(i), 2) == 1) then
        sum_val = sum_val + lst(i)
      end if
    end do
    solution = sum_val
  end function solution

end program solution