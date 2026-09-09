program smallest_change_demo
  implicit none
  integer, parameter :: MAX_LEN = 100
  integer :: arr_len
  integer, dimension(MAX_LEN) :: arr
  integer :: result

  ! Read input
  read(*,*) arr_len
  read(*,*) (arr(i), i=1,arr_len)

  ! Call the function
  result = smallest_change(arr_len, arr)

  ! Print output
  print *, result

contains

  function smallest_change(arr_len, arr) result(res)
    implicit none
    integer, intent(in) :: arr_len
    integer, intent(in), dimension(:) :: arr
    integer :: res
    integer :: i
    
    res = 0
    do i = 1, arr_len/2
      if (arr(i) /= arr(arr_len - i + 1)) then
        res = res + 1
      end if
    end do
  end function smallest_change

end program smallest_change_demo