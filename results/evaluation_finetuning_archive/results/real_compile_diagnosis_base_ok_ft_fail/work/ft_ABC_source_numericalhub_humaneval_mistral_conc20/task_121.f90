program test_solution
  implicit none
  integer, parameter :: i4b = selected_int_kind(9)
  integer(i4b) :: lst_len
  integer(i4b), allocatable :: lst(:)
  integer(i4b) :: result
  
  read(*,*) lst_len
  allocate(lst(lst_len))
  read(*,*) (lst(i), i=1, lst_len)
  
  result = solution(lst_len, lst)
  print *, result
  
contains

  function solution(lst_len, lst) result(res)
    implicit none
    integer(i4b), intent(in) :: lst_len
    integer(i4b), intent(in) :: lst(:)
    integer(i4b) :: res
    integer(i4b) :: i
    
    res = 0
    do i = 1, lst_len
      if (mod(i, 2) /= 0 .and. mod(lst(i), 2) /= 0) then
        res = res + lst(i)
      end if
    end do
  end function solution

end program test_solution